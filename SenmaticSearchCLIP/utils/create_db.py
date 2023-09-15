import mysql.connector

# Connect to the MySQL database server
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    port='3306'
)
cursor = conn.cursor()

# Create the new database
cursor.execute("CREATE DATABASE HCMC_AI_2023")
cursor.execute('''
    Use  HCMC_AI_2023
''')

cursor.execute('''
    CREATE TABLE images (
        ID INT PRIMARY KEY,
        image_path TEXT 
    )
''')

# Close the connection
conn.close()