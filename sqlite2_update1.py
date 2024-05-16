import sqlite3
import os

# Path to the text file (use the absolute path)
file_path = 'C:/database/shoeinsert.txt/datashoe.txt'

# Check if the file exists and is readable
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist or cannot be accessed.")

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
            print(f"Name: {name}, Size: {size}")  # Debugging
            
            # Create and execute insert query
            sql = "INSERT INTO brands (name, size) VALUES (?, ?)"
            cursor.execute(sql, (name.strip(), size.strip()))
    
    # Commit the changes
    conn.commit()
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    conn.close()
