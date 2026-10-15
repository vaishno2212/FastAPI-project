import sqlite3
from schemas import Ship, UpdateShipment


class Database:
    def __init__(self, db_name: str = "supply.db"):
        self.con = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_table("shipments")

    def create_table(self, name: str):
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT, 
            weight REAL, 
            status TEXT
        )
        """)
        self.con.commit()

    def new_shipment(self, shipment: Ship):
        self.cur.execute(
            """   
            INSERT INTO shipments (weight, content, status)
            VALUES (:weight, :content, :status)
            """,
            {
                "weight": shipment.weight,
                "content": shipment.content,
                "status": shipment.status.value if hasattr(shipment.status, "value") else str(shipment.status),
            },
        )
        self.con.commit()
        return self.cur.lastrowid

    def update_shipment(self, sid: int, shipment: UpdateShipment):
        self.cur.execute(
            """
            UPDATE shipments 
            SET content = :content, weight = :weight
            WHERE id = :sid
            """,
            {
                "content": shipment.content,
                "weight": shipment.weight,
                "sid": sid,
            },
        )
        self.con.commit()
        return self.cur.rowcount


if __name__ == "__main__":
    db = Database("supply.db")
    print("Database connected and table verified.")
