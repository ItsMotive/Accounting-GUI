from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk
import csv

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    payment_values = []
    if file_path:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            try: 
                for entry in reader:
                    for col in entry:
                        print(col)
            except Exception as e:
                # Display error message
                print(e)   
    print(payment_values)
                
# Create the main window
root = tk.Tk()
root.title("PostgreSQL Table Display and Payment Entry")

# Configure rows and columns to expand and fill available space
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Add Payment Section
add_payment_frame = ttk.LabelFrame(root, text="Add Payment")
add_payment_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
add_payment_frame.rowconfigure(0, weight=1)
add_payment_frame.columnconfigure(0, weight=1)
add_payment_frame.columnconfigure(1, weight=1)

# Payment Method
payment_method_label = ttk.Label(add_payment_frame, text="Payment Method:")
payment_method_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
payment_method_entry = ttk.Entry(add_payment_frame)
payment_method_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")


# Create a button widget
button = tk.Button(root, text="Import From CSV", command=open_file)
button.grid(pady=20)

# Start the GUI event loop
root.mainloop()

# Prints each Row and Col number and field
def get_list_of_payments() -> list:
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    all_entries = []
    
    if file_path:
        
        # Opens File
        with open(file_path, 'r') as file:
            
            # Sets up csv reader
            reader = csv.reader(file)
            
            # Skips header
            next(reader)
            try:
                for col, entry in enumerate(reader):
                    
                    for column, row in enumerate(entry):
                        print('Row {}: Col {} - {}'.format(col, column, row))
                        
            except Exception as e:
                print(e)
        
    return all_entries  