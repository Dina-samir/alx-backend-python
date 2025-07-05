import csv
import uuid
import mysql.connector
import requests
from io import StringIO
from mysql.connector import errorcode

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"
CSV_URL = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20250704%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250704T165008Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a5402de9c2c9e9c1fd22fa262f44a7ebf2c2c800e5ef48ab16f24d5c8784ac51"

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword", 
    )


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database `{DB_NAME}` created or already exists.")
    finally:
        cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword", 
        database=DB_NAME
    )

def create_table(connection):
    cursor = connection.cursor()
    create_stmt = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX(user_id)
    )
    """
    cursor.execute(create_stmt)
    print(f"Table `{TABLE_NAME}` created or already exists.")
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    insert_stmt = f"""
    INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(insert_stmt, data)
    connection.commit()
    print(f"{cursor.rowcount} rows inserted.")
    cursor.close()

def fetch_csv_data():
    """Fetches and parses the CSV from the remote URL."""
    response = requests.get(CSV_URL)
    response.raise_for_status()
    csv_content = response.content.decode('utf-8')
    reader = csv.DictReader(StringIO(csv_content))
    rows = []
    for row in reader:
        user_id = row.get("user_id") or str(uuid.uuid4())
        name = row["name"]
        email = row["email"]
        age = float(row["age"])
        rows.append((user_id, name, email, age))
    return rows

if __name__ == "__main__":
    try:
        root_conn = connect_db()
        create_database(root_conn)
        root_conn.close()

        db_conn = connect_to_prodev()
        create_table(db_conn)

        data = fetch_csv_data()
        insert_data(db_conn, data)
        db_conn.close()

        print("Database seeding complete.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(f"Error: {err}")
    except requests.RequestException as req_err:
        print(f"Failed to fetch CSV: {req_err}")
