import mysql.connector

def connect_db():
    """
    Connect to the MySQL database.
    Database will be created in main.py if it doesn't exist.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kalisa@53",  
            database="maternal_health_db"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"\n! Database connection error: {err}")
        
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalisa@53"
            )
            return connection
        except mysql.connector.Error as err:
            print(f"\n! Base connection error: {err}")
            return None