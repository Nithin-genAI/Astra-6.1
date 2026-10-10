import sqlite3
import os

# Define the path to the database file
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

# Connect to the SQLite database
connection = sqlite3.connect(db_path)

try:
    # Create table if it doesn't exist
    raw_query = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)'
    connection.execute(raw_query)

    # Add items to the database
    for i in range(5):
        raw_query = f"INSERT INTO items (name) VALUES ('item{i}')"
        connection.execute(raw_query)
    connection.commit()

finally:
    # Close the database connection
    connection.close()