import sqlite3
import functools

#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
       query= kwargs.get("query")
       if query:
        print(f"Executing SQL Query: {query}")
       else:
        print("No query found to log.")
       result= func( *args, **kwargs)
       return result 
    return wrapper



@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")