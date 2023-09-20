import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")
connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
cursor = connection.cursor()
try:

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS my_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equation VARCHAR(255) NOT NULL,
        result INT NOT NULL
    )
    """
    cursor.execute(create_table_query)

    # Read data from the "sums.txt" file
    with open("sums.txt", "r") as file:
        lines = file.readlines()

    # Initialize a variable to store the sum of results
    total_sum = 0

    # Process and insert data into the "my_table" table
    for line in lines:
        parts = line.strip().split('=')  # Split the line by '='
        if len(parts) == 2:
            equation, result = parts[0].strip(), parts[1].strip()
            query = "INSERT INTO my_table (equation, result) VALUES (%s, %s)"
            cursor.execute(query, (equation, result))

            # Add the result to the total sum
            total_sum += int(result)

    # Commit the changes to the database
    connection.commit()

    # Insert the total sum into the table
    total_sum_query = "INSERT INTO my_table (equation, result) VALUES (%s, %s)"
    cursor.execute(total_sum_query, ("Total Sum", str(total_sum)))

    # Commit the total sum to the database
    connection.commit()

    print("Data inserted successfully")
    print(f"Sum of all results: {total_sum}")

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
