#!/usr/bin/python3

import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch one page of users from the database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootpassword",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

def lazy_paginate(page_size):
    """
    Generator that lazily fetches and yields paginated user data.
    """
    offset = 0
    while True:  # <-- Only loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

