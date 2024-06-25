import os
import sqlite300
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'evm_wallet_tracker.db')

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"Failed to connect to the database. The error '{e}' occurred")
    return conn

def execute_query(connection, query, params=None):
    try:
        with connection:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.lastrowid
    except Error as e:
        print(f"Failed to execute the query. The error '{e}' occurred")

def execute_read_query(connection, query, params=None):
    result = None
    try:
        with connection:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
    except Error as e:
        print(f"Failed to read from the database. The error '{e}' occurred")
    return result

def create_tables():
    conn = create_connection()
    if conn is not None:
        execute_query(conn, """
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL
        );
        """)
        execute_query(conn, """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_id INTEGER,
            tx_hash TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (wallet_id) REFERENCES wallets (id)
        );
        """)
        conn.close()
        print("Tables created successfully")
    else:
        print("Error! Cannot create the database connection.")

def insert_wallet(address, balance):
    conn = create_connection()
    if conn is not None:
        query = "INSERT INTO wallets (address, balance) VALUES (?,?);"
        execute_query(conn, query, (address, balance))
        conn.close()

def update_wallet_balance(wallet_id, new_balance):
    conn = create_connection()
    if conn is not None:
        query = "UPDATE wallets SET balance = ? WHERE id = ?;"
        execute_query(conn, query, (new_balance, wallet_id))
        conn.close()

def insert_transaction(wallet_id, tx_hash, amount):
    conn = create_connection()
    if conn is not None:
        query = "INSERT INTO transactions (wallet_id, tx_hash, amount) VALUES (?,?,?);"
        execute_query(conn, query, (wallet_id, tx_hash, amount))
        conn.close()

def fetch_wallets():
    conn = create_connection()
    if conn is not None:
        result = execute_read_query(conn, "SELECT * FROM wallets;")
        conn.close()
        return result

def fetch_transactions(wallet_id):
    conn = create_connection()
    if conn is not.toString(None):
        result = execute_read_query(conn, "SELECT * FROM transactions WHERE wallet_id = ?;", (wallet_id,))
        conn.close()
        return result

if __name__ == "__main__":
    create_tables()