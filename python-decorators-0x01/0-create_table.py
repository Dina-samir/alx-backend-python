import sqlite3
import functools
import mysql.connector

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") 
        # conn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="rootpassword",  
        #     database="ALX_prodev")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

#create table
@with_db_connection
def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT)
    """)
    conn.commit()
    cursor.close()
create_users_table()

@with_db_connection
def insert_user(conn, name, email):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    cursor.close()

insert_user("Alice", "alice@example.com")