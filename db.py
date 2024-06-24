import os
import sqlite3
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
        print(f"The error '{e}' occurred")
    return conn

def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query, params=None):
    cursor = connection.cursor()
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

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
        print("Tables created successfully")
    else:
        print("Error! cannot create the database connection.")

def insert_wallet(address, balance):
    conn = create_connection()
    query = "INSERT INTO wallets (address, balance) VALUES (?,?);"
    execute_query(conn, query, (address, balance))

def update_wallet_balance(wallet_id, new_balance):
    conn = create_connection()
    query = "UPDATE wallets SET balance = ? WHERE id = ?;"
    execute_query(conn, query, (new_balance, wallet_id))

def insert_transaction(wallet_id, tx_hash, amount):
    conn = create_connection()
    query = "INSERT INTO transactions (wallet_id, tx_hash, amount) VALUES (?,?,?);"
    execute_query(conn, query, (wallet_id, tx_hash, amount))

def fetch_wallets():
    conn = create_connection()
    return execute_read_query(conn, "SELECT * FROM wallets;")

def fetch_transactions(wallet_id):
    conn = create_connection()
    return execute_read_query(conn, "SELECT * FROM transactions WHERE wallet_id = ?;", (wallet_id,))

if __name__ == "__main__":
    create_tables()