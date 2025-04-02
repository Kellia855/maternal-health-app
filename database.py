import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="!anyika@12#2005",
        database="mhs_sys"
    )

