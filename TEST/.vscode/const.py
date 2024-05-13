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
            DELETE FROM public."Test" WHERE pk IN %s;;
        """
