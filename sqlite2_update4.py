import sqlite3
import os
import time

# Path to the text file (use the absolute path)
file_path = 'C:/database/shoeinsert.txt/datashoe.txt'

# Check if the file exists and is readable
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist or cannot be accessed.")

# Function to insert data into the database
def insert_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('shoes.db')
    cursor = conn.cursor()

    try:
        # Read shoe values from the text file
        with open(file_path, 'r') as file:
            for line in file:
                # Strip any leading/trailing whitespace
                stripped_line = line.strip()
                
                # Skip empty lines
                if not stripped_line:
                    continue
                
                # Split the line into name and size
                parts = stripped_line.split(',')
                
                # Check if the line was split into exactly two parts
                if len(parts) != 2:
                    print(f"Skipping malformed line: {line}")
                    continue
                
                name, size = parts
                name = name.strip()
                size = size.strip()
                print(f"Name: {name}, Size: {size}")  # Debugging
                
                # Check if a record with the same shoe name and size already exists
                sql_check = "SELECT COUNT(*) FROM brands WHERE name = ? AND size = ?"
                cursor.execute(sql_check, (name, size))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    # Create and execute insert query
                    sql_insert = "INSERT INTO brands (name, size) VALUES (?, ?)"
                    cursor.execute(sql_insert, (name, size))
                    print(f"Inserted: {name}, {size}")
                else:
                    print(f"Skipping duplicate: {name}, {size}")
        
        # Commit the changes
        conn.commit()
        print("Data inserted successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

# Attempt to insert data, with retry logic for database locks
def insert_with_retry():
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            insert_data()
            break  # Exit the loop if insertion is successful
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries += 1
                print(f"Retrying ({retries}/{max_retries})...")
                time.sleep(1)  # Wait for a short period before retrying
            else:
                raise  # Raise other OperationalError exceptions
    else:
        print("Max retries exceeded. Unable to insert data.")

# Perform data insertion with retry logic
insert_with_retry()
