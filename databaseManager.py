import sqlite3

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("finance.db")
        self.connection.row_factory = sqlite3.Row
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
                initial_balance INTEGER NOT NULL
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
                amount INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE RESTRICT
                
            )
                
        
        
        
        """)


        self.connection.commit()

#Categories methods

    def initialize_categories(self, default_categories, user_id):
        self.cursor.execute("SELECT COUNT(0) FROM categories WHERE user_id = ?", (user_id,))
        count = self.cursor.fetchone()[0]

        new_data = []
        for cat_name, cat_type in default_categories:
            new_data.append((cat_name, cat_type, user_id))


        if count == 0:
            self.cursor.executemany("INSERT INTO categories (category_name, category_type, user_id) VALUES (?,?,?)", new_data)


            self.connection.commit()

    def load_categories(self, user_id):
        self.cursor.execute("SELECT category_id, category_name, category_type FROM categories WHERE user_id = ?", (user_id,))
        rows = self.cursor.fetchall()

        return rows

    def add_category(self, category_name, category_type, user_id):
        self.cursor.execute("""
            INSERT into categories (category_name, category_type, user_id) VALUES (?,?,?) """,
                            (category_name, category_type, user_id))

        self.connection.commit()

        new_id = self.cursor.lastrowid

        return new_id

    def delete_category(self, category_id):
        self.cursor.execute("DELETE FROM categories WHERE category_id = ?",
                            (category_id,))
        self.connection.commit()

#Transaction methods

    def add_transaction(self, transaction_type, amount, category_id, date, description, user_id ):
        self.cursor.execute("""
                    INSERT into transactions (transaction_type, amount, category_id, date, description, user_id) VALUES (?,?,?,?,?,?)""",
                            (transaction_type, amount, category_id, date, description, user_id))

        self.connection.commit()

        new_id = self.cursor.lastrowid

        return new_id


    def load_transactions(self, user_id):
        self.cursor.execute("SELECT transaction_id, transaction_type, amount, category_id, date, description FROM transactions WHERE user_id = ?",
                            (user_id,))
        rows = self.cursor.fetchall()

        return rows


    def delete_transaction(self, transaction_id):
        self.cursor.execute("DELETE FROM transactions WHERE transaction_id =?",
                            (transaction_id,))

        self.connection.commit()



    def update_transaction_amount(self, new_amount, transaction_id, user_id):

        self.cursor.execute("UPDATE transactions SET amount = ? WHERE transaction_id = ? AND user_id =?",
                            (new_amount,transaction_id, user_id))

        self.connection.commit()



    def update_transaction_category(self, new_category_id, transaction_id, user_id):
        self.cursor.execute("UPDATE transactions SET category_id = ? WHERE transaction_id = ? AND user_id = ?",
                            (new_category_id, transaction_id, user_id))

        self.connection.commit()


    def update_transaction_date(self, new_date, transaction_id, user_id ):
        self.cursor.execute("UPDATE transactions SET date = ? WHERE transaction_id = ? AND user_id = ?",
                            (new_date.strftime("%Y-%m-%d"), transaction_id, user_id) )

        self.connection.commit()


    def update_transaction_description(self, new_description, transaction_id, user_id):
        self.cursor.execute("UPDATE transactions SET description = ? WHERE transaction_id = ? AND user_id = ?",
                            (new_description, transaction_id, user_id))

        self.connection.commit()









# User methods

    def get_user(self):

        self.cursor.execute("SELECT * FROM users LIMIT 1")
        row = self.cursor.fetchone()


        return row

    def insert_user(self, username, currency, initial_balance):
        self.cursor.execute("""
            INSERT INTO users (username, currency, initial_balance) VALUES (?, ?, ?)""",
                            (username, currency, initial_balance)
                            )

        self.connection.commit()

        new_id = self.cursor.lastrowid
        return new_id


