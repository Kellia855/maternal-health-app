import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kalisa@53",
        database="mhs_sys"
    )

