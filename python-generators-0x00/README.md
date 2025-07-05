# 📊 User Data Streaming and Processing with Python & MySQL

This project demonstrates memory-efficient ways to interact with a MySQL database using Python generators, decorators, and context managers. It includes scripts for seeding data, streaming rows and batches, paginating lazily, and computing aggregates like average age — all without loading the entire dataset into memory.

---

## 📁 Contents

- [`seed.py`](./seed.py) — Seeds the MySQL database with user data from a CSV file.
- [`0-stream_users.py`](./0-stream_users.py) — Streams rows one by one using a generator.
- [`1-batch_stream.py`](./1-batch_stream.py) — Processes user data in batches with a generator.
- [`2-lazy_paginate.py`](./2-lazy_paginate.py) — Lazily fetches paginated data from MySQL.
- [`3-average_age.py`](./4-stream_ages.py) — Calculates the average age of users using a generator and memory-efficient logic.

---

## 💪 Requirements

- Python 3.x
- MySQL server (local or Docker)
- [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/)

```bash
 pip install mysql-connector-python requests
```

---

## 📄️ Database Setup

The database used is `ALX_prodev` with one table:

```sql
CREATE TABLE user_data (
  user_id CHAR(36) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  age DECIMAL(5,2) NOT NULL,
  INDEX(user_id)
);
```

---

## 🔀 1. Seeding the Database (`seed.py`)

Seeds the database from a CSV file (`user_data.csv`) and creates the table if it doesn’t exist.

### Prototype Functions:

```python
def connect_db()
def create_database(connection)
def connect_to_prodev()
def create_table(connection)
def insert_data(connection, file_path)
```

### Usage:

```bash
python seed.py
```

---

## 🔄 2. Stream Users Row by Row (`0-stream_users.py`)

### Objective:

Fetch and yield each user row one-by-one using a generator.

### Prototype:

```python
def stream_users()
```

---

## 📦 3. Batch Processing Users (`1-batch_stream.py`)

### Objective:

Fetch users in batches and process each batch to filter users with age > 25.

### Prototypes:

```python
def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
```

---

## 📚 4. Lazy Pagination (`2-lazy_paginate.py`)

### Objective:

Simulate pagination by lazily fetching data from the table page by page using offset.

### Prototypes:

```python
def paginate_users(page_size, offset)
def lazy_paginate(page_size)
```

- Uses **only one loop**
- Uses `yield` for memory-efficient pagination

---

## 🧲 5. Average Age with Generators (`3-average_age.py`)

### Objective:

Compute the average age of all users without loading all records into memory.

### Features:

- Uses a generator `stream_user_ages()` to yield ages one at a time
- Uses a `contextmanager` for DB connection
- Uses a `decorator` for logging
- Uses **only 2 loops**
- Avoids SQL `AVG()`

### Prototypes:

```python
def stream_user_ages()
def compute_average_age()
```

---

## 📌 Sample Output

```bash
Running compute_average_age...
Running stream_user_ages...
Average age of users: 48.52
```

---

## 📌 Notes

- All database credentials are assumed to be:
  - User: `root`
  - Password: `rootpassword`
  - Host: `localhost`
- You can change these inside the scripts to fit your environment.
- CSV format expected: `user_id,name,email,age` (UUIDs can be blank and will be auto-generated)
- The used data from [data.csv]("https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20250704%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250704T165008Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a5402de9c2c9e9c1fd22fa262f44a7ebf2c2c800e5ef48ab16f24d5c8784ac51")
---

## 🤝 Author

Dina Samir — [GitHub](https://github.com/Dina-samir)

---

