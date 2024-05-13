from datetime import datetime
import tkinter as tk
from tkinter import ttk
import psycopg2

from const import (
    ADD_QUERY,
    DATABASE_NAME,
    DELETE_QUERY,
    HOST,
    PASSWORD,
    PORT,
    TABLE_QUERY,
    USERNAME,
)


class SortingTreeview(ttk.Treeview):
    """
    A custom Treeview widget that allows sorting by clicking on column headers.
    """

    def __init__(self, master=None, **kw):
        """
        Initialize the SortingTreeview widget.

        Parameters:
            master (tkinter.Tk or tkinter.Frame): The parent widget.
            **kw: Additional keyword arguments to configure the Treeview.

        Attributes:
            columns (list): List to store column identifiers.
            sort_column (str or None): The currently sorted column identifier.
            sort_descending (bool): Flag indicating sorting order (ascending or descending).
        """
        super().__init__(master, **kw)
        self.heading("#0", command=lambda: self.sort_treeview("#0", False))
        self.bind("<ButtonRelease-1>", self.header_click)
        self.columns = []
        self.sort_column = None
        self.sort_descending = False

    def header_click(self, event):
        """
        Handle the click event on column headers to trigger sorting.

        Parameters:
            event (tkinter.Event): The event object containing information about the click.
        """
        region = self.identify("region", event.x, event.y)
        if region == "heading":
            column = self.identify_column(event.x)
            self.sort_treeview(column, self.sort_column == column)

    def sort_treeview(self, column, reverse):
        """
        Sort the Treeview based on the specified column and sorting order.

        Parameters:
            column (str): The column identifier to sort by.
            reverse (bool): Flag indicating sorting order (True for descending, False for ascending).
        """
        data = [(self.item(item)["text"], item) for item in self.get_children("")]
        data.sort(reverse=reverse)
        for index, (_, item) in enumerate(data):
            self.move(item, "", index)
        if reverse:
            self.heading(column, command=lambda: self.sort_treeview(column, False))
        else:
            self.heading(column, command=lambda: self.sort_treeview(column, True))
        self.sort_column = column


def display_table():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    try:
        # Execute a SQL query to fetch data from a table
        cur.execute(TABLE_QUERY)

        # Check if cur.description is not None and has valid data
        if cur.description:
            col_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            # Display the table in the GUI
            display_gui(rows, col_names)
        else:
            # Display an error message if cur.description is None or empty
            error_label.config(text="No data available in the table.")
    except Exception as e:
        # Display error message
        error_label.config(text="Error: " + str(e))

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()


def display_gui(rows, col_names):
    # Close existing table window if it exists
    if hasattr(display_gui, "table_window") and display_gui.table_window.winfo_exists():
        display_gui.table_window.destroy()

    # Create a new window for displaying the table
    display_gui.table_window = tk.Toplevel(root)
    display_gui.table_window.title("Accounting Database")

    # Create a SortingTreeview widget to display the table with sorting capability
    tree = SortingTreeview(display_gui.table_window)
    tree["columns"] = col_names
    tree["show"] = "headings"

    # Add columns to the treeview
    for col_name in col_names:
        tree.heading(col_name, text=col_name)
        tree.column(
            col_name, width=100, anchor="center"
        )  # Adjust column width and alignment as needed

    # Add rows to the treeview
    for row in rows:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill=tk.BOTH)

    # Refresh Button
    refresh_button = ttk.Button(
        display_gui.table_window, text="Refresh", command=display_table
    )
    refresh_button.pack(side="bottom", pady=10)


def add_payment():
    # Get values from entry fields
    payment_values = [
        item_name_entry.get(),
        amount_entry.get(),
        merchant_entry.get(),
        datetime.strptime(purchase_date_entry.get(), "%m-%d-%Y").date(),
        payment_method_entry.get(),
    ]

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    try:
        # Execute an SQL query to insert new payment data into the table
        cur.execute(
            ADD_QUERY,
            payment_values,
        )

        # Commit the transaction
        conn.commit()

        # Display success message
        success_label.config(text="Payment added successfully!")

    except Exception as e:
        # Display error message
        success_label.config(text="Error: " + str(e))

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()


def open_delete_window():
    global entry_pks, success_label, error_label  # Declare global variables

    # Create the main window for deleting items
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Payment by PKs")

    # Configure rows and columns to expand and fill available space
    delete_window.rowconfigure(0, weight=1)
    delete_window.columnconfigure(0, weight=1)

    # PKs Entry
    entry_label = ttk.Label(delete_window, text="Enter PKs (comma-separated):")
    entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_pks = ttk.Entry(delete_window)
    entry_pks.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Delete Button
    delete_button = ttk.Button(delete_window, text="Delete Items", command=delete_items)
    delete_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    # Success/Error Message Labels (global scope)
    success_label = ttk.Label(delete_window, foreground="green")
    success_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    error_label = ttk.Label(delete_window, foreground="red")
    error_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)


def delete_items():
    global success_label, error_label  # Access global labels

    selected_pks = entry_pks.get()
    if not selected_pks:
        error_label.config(text="Please enter valid PK values.")
        return

    # Convert the comma-separated PKs to a list
    pk_list = selected_pks.split(",")
    pk_list = [pk.strip() for pk in pk_list]

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    try:
        # Execute an SQL query to delete items with the specified PKs
        cur.execute(DELETE_QUERY, (tuple(pk_list),))
        conn.commit()

        # Display success message
        success_label.config(
            text=f"Items with PKs {', '.join(pk_list)} deleted successfully!"
        )

    except Exception as e:
        # Display error message
        success_label.config(text="Error: " + str(e))

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()


# Create the main window
root = tk.Tk()
root.title("PostgreSQL Table Display and Payment Entry")


# Configure rows and columns to expand and fill available space
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Display Table Button
display_button = ttk.Button(root, text="Display Table", command=display_table)
display_button.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Add Payment Section
add_payment_frame = ttk.LabelFrame(root, text="Add Payment")
add_payment_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
add_payment_frame.rowconfigure(0, weight=1)
add_payment_frame.columnconfigure(0, weight=1)
add_payment_frame.columnconfigure(1, weight=1)

# Item Name
item_name_label = ttk.Label(add_payment_frame, text="Item Name:")
item_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
item_name_entry = ttk.Entry(add_payment_frame)
item_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Amount
amount_label = ttk.Label(add_payment_frame, text="Amount:")
amount_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
amount_entry = ttk.Entry(add_payment_frame)
amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# Merchant
merchant_label = ttk.Label(add_payment_frame, text="Merchant:")
merchant_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
merchant_entry = ttk.Entry(add_payment_frame)
merchant_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

# Purchase Date
purchase_date_label = ttk.Label(add_payment_frame, text="Purchase Date (MM-DD-YYYY):")
purchase_date_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
purchase_date_entry = ttk.Entry(add_payment_frame)
purchase_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

# Payment Method
payment_method_label = ttk.Label(add_payment_frame, text="Payment Method:")
payment_method_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
payment_method_entry = ttk.Entry(add_payment_frame)
payment_method_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

# Add Payment Button
add_payment_button = ttk.Button(
    add_payment_frame, text="Add Payment", command=add_payment
)
add_payment_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

# Delete Payments Button
delete_payments_button = ttk.Button(
    root, text="Delete Payments", command=open_delete_window
)
delete_payments_button.grid(row=8, column=0, padx=10, pady=10)

# Success/Error Message Label
success_label = ttk.Label(root, foreground="green")
success_label.grid(row=9, column=0, sticky="ew", padx=10, pady=10)

error_label = ttk.Label(root, foreground="red")
error_label.grid(row=10, column=0, sticky="ew", padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
