import mysql.connector

def connect_db():
    """
    Connect to the MySQL database.
    Database will be created in main.py if it doesn't exist.
    """
    try:
        # First try to connect to the specific database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kalisa@53",  
            database="maternal_health_management_system"  
        )
        print("* Connected to maternal_health_management_system database!")
        return connection
    except mysql.connector.Error as err:
        print(f"* Note: {err}")
        print("* Attempting to connect without database specification...")
        
        # If that fails, try connecting without specifying the database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalisa@53"
            )
            print("* Basic database connection successful!")
            return connection
        except mysql.connector.Error as err:
            print(f"\n! Base connection error: {err}")
            return None