import sqlite3

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("finance.db")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                currency TEXT NOT NULL,
                initial_balance REAL NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL,
                category_type TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE RESTRICT
                
            )
                
        
        
        
        """)


        self.connection.commit()


