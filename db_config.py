import sqlite3
import os

def init_sqlite(app):
    try:
        # Create or connect to database.db in the root folder
        db_path = os.path.join(os.path.dirname(__file__), 'database.db')
        connection = sqlite3.connect(db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row # Returns dict-like objects
        print("Connected to SQLite database")
        
        # Initialize tables if they don't exist
        with open(os.path.join(os.path.dirname(__file__), 'database.sql'), 'r') as f:
            connection.executescript(f.read())
            
        return connection
    except sqlite3.Error as e:
        print("Error while connecting to SQLite:", e)
        return None
