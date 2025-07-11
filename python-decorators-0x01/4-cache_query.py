import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") 
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query= kwargs.get("query")
        value = query_cache.get(query)
        if value is not None:
            return query_cache[query]
        else:
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result

    return wrapper

@cache_query
@with_db_connection
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")