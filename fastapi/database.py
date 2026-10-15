import sqlite3

# connect to local sqlite database
connection = sqlite3.connect("sql.db")
cur = connection.cursor()

# create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS shipment (
    id INTEGER PRIMARY KEY,
    weight REAL,
    content TEXT, 
    status TEXT
)
""")
connection.commit()

# insert sample records using ? placeholders to avoid sql injection
cur.execute("""
INSERT OR REPLACE INTO shipment (id, weight, content, status)
VALUES (?, ?, ?, ?)
""", (1273, 5.1, "books", "pending"))

cur.execute("""
INSERT OR REPLACE INTO shipment (id, weight, content, status)
VALUES (?, ?, ?, ?)
""", (1274, 22.0, "refrigerator", "delivered"))
connection.commit()

# fetch all rows
cur.execute("SELECT * FROM shipment")
all_data = cur.fetchall()
print("All shipments:", all_data)

# query a single record by id
target_id = 1273
cur.execute("SELECT * FROM shipment WHERE id = ?", (target_id,))
single_row = cur.fetchone()
print(f"Shipment #{target_id}:", single_row)

connection.close()
