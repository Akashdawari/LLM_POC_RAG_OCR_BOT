import sqlite3
import os

def get_db_connection(db_name='database/users.db'):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_name), exist_ok=True)

    # Establish connection to the SQLite database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Check if the users table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = c.fetchone()

    # Create the users table if it does not exist
    if not table_exists:
        c.execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            email TEXT,
            password TEXT,
            reason TEXT
        )
        ''')
        # Commit the changes only if the table was created
        conn.commit()

    # Return the connection object
    return conn
