#!/usr/bin/python3

import mysql.connector

def stream_users():
    """Generator that yields rows one by one from user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootpassword",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row  # Yield one row at a time

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")


if __name__ == "__main__":
    try:
        for user in stream_users():
            print(user)
    except Exception as e:
        print(e)
