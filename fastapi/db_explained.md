# Understanding `db.py`

This file is responsible for connecting your Python application to your PostgreSQL database. It defines a `Database` class that allows you to easily create tables and insert or update data. Here is a beginner-friendly breakdown of what each line does.

### Imports
```python
import psycopg2
import psycopg2.extras
from schemas import Ship, UpdateShipment
```
- **`import psycopg2`**: This imports the PostgreSQL database adapter for Python. It is the tool that lets Python "talk" to a Postgres database.
- **`import psycopg2.extras`**: This imports extra utilities for psycopg2. We use it specifically for a feature called `DictCursor` (which allows you to access database rows like Python dictionaries instead of just a list of values).
- **`from schemas import Ship, UpdateShipment`**: This imports two classes (likely Pydantic models) from a file called `schemas.py` in your project. These are used to validate and structure the data (like `weight` and `content`) before it gets sent to the database.

### The Database Class & Initialization
```python
class Database:
    def __init__(self, db_name):
        # db_name here can be a full postgresql connection string
        self.con = psycopg2.connect(db_name)
        self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.create_table("shipments")
```
- **`class Database:`**: This creates a blueprint (a Class) for your database connection.
- **`def __init__(self, db_name):`**: This is a special function called a "constructor". It runs automatically whenever you create a new `Database` object. The `db_name` parameter represents your database connection string.
- **`self.con = psycopg2.connect(db_name)`**: This line actually opens the connection to your PostgreSQL database using the provided string. `self.con` saves this connection so it can be used later.
- **`self.cur = ... cursor(...)`**: A "cursor" is like a pointer or messenger that executes SQL commands on the database. By using `DictCursor`, the data returned from queries will act like Python dictionaries (e.g., `row['content']`), making it much easier to read.
- **`self.create_table("shipments")`**: The moment you connect to the database, this calls the `create_table` method (defined below) to make sure the "shipments" table actually exists before you start doing anything else.

### Creating a Table
```python
    def create_table(self, name: str):
        self.cur.execute(f"""
CREATE TABLE IF NOT EXISTS {name}
(id SERIAL PRIMARY KEY,
content TEXT, 
weight REAL, 
status TEXT
)
""")
        self.con.commit()
```
- **`def create_table(self, name: str):`**: This defines a method that takes a table `name` as text (a string).
- **`self.cur.execute(...)`**: This tells the cursor to run an SQL command on the database. 
- **`CREATE TABLE IF NOT EXISTS {name}`**: This is the SQL command. It tells Postgres to create a new table with your chosen name, but *only* if it doesn't already exist.
- **`(id SERIAL PRIMARY KEY, ...)`**: This defines the columns of the table:
  - `id SERIAL PRIMARY KEY`: Every shipment needs a unique ID. `SERIAL` means Postgres will automatically generate an increasing number (1, 2, 3...) for every new row. `PRIMARY KEY` means this is the main identifier for the row.
  - `content TEXT`: A text column for what's inside the shipment.
  - `weight REAL`: A column for the weight of the shipment. `REAL` allows decimal numbers (like 12.5).
  - `status TEXT`: A text column describing the status (e.g., "Placed", "Shipped").
- **`self.con.commit()`**: In PostgreSQL, changes to the database (like creating a table, inserting, or updating data) aren't saved permanently until you "commit" them. Think of this like clicking the "Save" button in a Word document.

### Inserting Data (Creating a Shipment)
```python
    def new_shipment(self, shipments: Ship):
        self.cur.execute(
            """   
        INSERT INTO shipments
        (weight, content, status)
        VALUES 
        (%(weight)s, %(content)s, %(status)s)
        RETURNING id;
    """,
            {**shipments.model_dump(), "status": "Placed"},
        )
        self.con.commit()
        return self.cur.fetchone()[0]
```
- **`def new_shipment(self, shipments: Ship):`**: This method adds a new shipment to the database. It expects a `Ship` object.
- **`INSERT INTO shipments ... VALUES ...`**: The SQL command to insert a new row into the `shipments` table. 
- **`(%(weight)s, %(content)s, %(status)s)`**: These are placeholders. It is a security best practice to use placeholders instead of putting data directly into the SQL string. It prevents malicious users from "hacking" your database (a process called SQL Injection).
- **`RETURNING id;`**: A special PostgreSQL feature. After inserting a new row, it immediately gives back the `id` of the newly created shipment.
- **`{**shipments.model_dump(), "status": "Placed"}`**: This is the data that fills in those placeholders. `.model_dump()` turns your Pydantic `Ship` object into a regular dictionary. The `**` unpacks that dictionary, and we force the status to be `"Placed"`.
- **`return self.cur.fetchone()[0]`**: This fetches the result of `RETURNING id;`. `fetchone()` grabs the first row of results, and `[0]` gets the first column from that row, giving you the raw ID number to return back to your Python app.

### Updating Data
```python
    def update_shipment(self, sid: int, shipment: UpdateShipment):
        self.cur.execute(
            """
        UPDATE shipments SET 
        content = %(content)s, 
        weight = %(weight)s
        WHERE id = %(sid)s
""",
            {**shipment.model_dump(), "sid": sid},
        )
        self.con.commit()
        return self.cur.rowcount
```
- **`def update_shipment(...)`**: This method updates an existing shipment. It needs the ID of the shipment to update (`sid`) and the new data (`shipment`).
- **`UPDATE shipments SET ... WHERE id = %(sid)s`**: The SQL command to update a row. It says: "Change the content and weight in the shipments table, but *only* for the row where the `id` matches `sid`". 
- **`return self.cur.rowcount`**: After running the update, `rowcount` tells you how many rows were actually affected by the update. This is helpful to check if a shipment with that ID actually existed in the database.
