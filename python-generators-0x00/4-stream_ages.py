#!/usr/bin/python3

import mysql.connector
from contextlib import contextmanager
from functools import wraps

# Context Manager for database connection
@contextmanager
def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword",  
        database="ALX_prodev"
    )
    try:
        yield conn
    finally:
        conn.close()

# Optional Decorator for logging (just to demonstrate usage)
def log_step(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

# Generator: Stream user ages one by one
@log_step
def stream_user_ages():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:  # Loop 1
            yield row[0]
        cursor.close()

# Compute average age using generator (no full load)
@log_step
def compute_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1
    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    compute_average_age()
