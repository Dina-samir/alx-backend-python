#!/usr/bin/python3

import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the database.
    Each yield returns a list of rows.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootpassword",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

def batch_processing(batch_size):
    """
    Generator that filters and yields users over age 25
    from each batch yielded by stream_users_in_batches().
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:                             # loop 2
            if user[3] > 25:                            # assuming age is 4th column
                yield user                              # generator yield
