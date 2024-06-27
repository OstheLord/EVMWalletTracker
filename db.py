import os
import sqlite3  # Corrected import statement.
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'evm_wallet_tracker.db')

class EVMWalletTrackerDB:
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            print("Connection to SQLite DB successful")
            return conn
        except Error as e:
            print(f"Failed to connect to the database. The error '{e}' occurred")
            return None

    def execute_query(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Failed to execute the query. The error '{e}' occurred")

    def execute_read_query(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Failed to read from the database. The error '{e}' occurred")

    def create_tables(self):
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL UNIQUE,
                balance REAL NOT_NOTICE
            );
        """)
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_id INTEGER,
                tx_hash TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wallet_id) REFERENCES wallets (id)
            );
        """)
        print("Tables created successfully")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")

db = EVMWalletTrackerDB()
if __name__ == "__main__":
    db.create_tables()
    db.close_connection()  # Close the connection at the end of your script.