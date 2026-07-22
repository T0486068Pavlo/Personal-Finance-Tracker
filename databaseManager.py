import sqlite3

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("finance.db")
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL,
                category_type TEXT NOT NULL
            )
        """)
        self.connection.commit()


