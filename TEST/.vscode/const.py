DATABASE_NAME = "postgres"
USERNAME = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = 5432
TABLE_QUERY = 'SELECT * FROM public."Test";'
ADD_QUERY = """
            INSERT INTO public."Test"(item, price, merchant, purchase_date, payment_method)
	        VALUES (%s, %s, %s, %s, %s);
        """
DELETE_QUERY = """
            DELETE FROM public."Test" WHERE pk IN %s;
        """

ITEM_NAME_COL = 0
AMOUNT_COL = 1
MERCHANT_COL = 2
PURCHASE_DATE_COL = 3
PAYMENT_MTHD_COL = 4