import sqlite3
import os
from pathlib import Path
from src.models import Account, Transaction, Institution

#TABLES
accounts_table = '''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution_id INTEGER NOT NULL,
    account_number TEXT NOT NULL,
    type TEXT NOT NULL,
    currency TEXT NOT NULL,
    nickname TEXT
)
'''

transactions_table = '''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    category TEXT,
    transaction_type TEXT NOT NULL,
    transfer_reference_id INTEGER
)
'''
Institution_table = '''
CREATE TABLE IF NOT EXISTS institutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
)
'''

# 1. Create a database connection (this also creates the file if it doesn't exist)
def create_connection(db_file="pfainance.db"):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        # Make sure the data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        db_path = data_dir / db_file
        conn = sqlite3.connect(db_path)
        print(f"Connected to SQLite version: {sqlite3.version}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    
    return conn

# 2. Create a table
def create_table(conn, sql):
    """Create a simple accounts table"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")



# 3. Insert data into the table
def insert_account(conn, account: Account):
    """Insert a new account into the accounts table"""
    sql = '''INSERT INTO accounts(account_number, institution_id, type, currency, nickname)
             VALUES(?, ?, ?, ?, ?)'''
    try:
        cursor = conn.cursor()
        data=account.model_dump()
        print(data)
        values= (
            data["account_number"],
            data["institution_id"],
            data["type"],
            data["currency"],
            data["nickname"]
        )
        cursor.execute(sql, values)
        conn.commit()
        print(f"Account inserted with id: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting account: {e}")
        return None

def insert_transaction(conn, transaction: Transaction):
    """Insert a new account into the accounts table"""
    
    sql = '''INSERT INTO transactions(account_id,date, description, amount, currency, category, transaction_type, transfer_reference_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
    try:
        cursor = conn.cursor()
        data=transaction.model_dump()
        print(data)
        values= (
            data["account_id"],
            data["date"],
            data["description"],
            data["amount"],
            data["currency"],
            data["category"],
            data["transaction_type"],
            data["transfer_reference_id"]
        )
        cursor.execute(sql, values)
        conn.commit()
        print(f"Transaction inserted with id: {cursor.lastrowid}")
        return cursor.lastrowid
    
    except sqlite3.Error as e:
        print(f"Error inserting transaction: {e}")
        return None

def insert_institution(conn, institution: Institution):
    """Insert a new institution into the institutions table"""
    sql = '''INSERT INTO institutions(name, type) VALUES(?, ?)'''
    try:
        cursor = conn.cursor()
        data=institution.model_dump()
        print(data)
        values= (
            data["name"],
            data["type"]
        )
        cursor.execute(sql, values)
        conn.commit()
        print(f"Institution inserted with id: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting institution: {e}")
        return None

# 4. Query and display all accounts
def select_all_accounts(conn):
    """Query all rows in the accounts table"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        
        rows = cursor.fetchall()
        print("\nAll accounts:")
        for row in rows:
            print(f"ID: {row[0]}, Number: {row[1]}, Type: {row[2]}")
        
        return rows
    except sqlite3.Error as e:
        print(f"Error querying accounts: {e}")  
        return []





# Example usage
def main():
    # Create a connection to the database
    conn = create_connection()
    conn.execute(accounts_table)
    conn.execute(transactions_table)
    conn.execute(Institution_table)
    
    if conn is not None:
        # Insert some sample institutions
        institution1 = Institution(name="UBS", type="bank")
        institution2 = Institution(name="Revolut", type="bank")
        insert_institution(conn, institution1)
        insert_institution(conn, institution2)
        
        # Insert some sample accounts
        account1 = Account(account_number="1234567890", institution_id=1, type="checking",  currency="CHF", nickname="Checking")
        account2 = Account(account_number="0987654321", institution_id=1, type="savings", currency="CHF", nickname="Savings")

        
        insert_account(conn, account1)
        insert_account(conn, account2)

        # Insert some sample transactions
        transaction1 = Transaction(account_id=1, date="2021-01-01", description="Transaction 1", amount=100, currency="CHF", category="Food", transaction_type="deposit")
        transaction2 = Transaction(account_id=1, date="2022-01-01", description="Transaction 2", amount=200, currency="CHF", transaction_type="deposit")
        insert_transaction(conn, transaction1)
        insert_transaction(conn, transaction2)
        # Query and display all accounts
        select_all_accounts(conn)
        
        # Close the connection
        conn.close()
        print("Database connection closed")
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()

# Account and Institution are written first
# trasnasciton are written based on accounts
# Balance is writtern 