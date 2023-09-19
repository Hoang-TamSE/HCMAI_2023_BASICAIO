import mysql.connector

# Connect to the MySQL database server
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    port='3306'
)
cursor = conn.cursor()

cursor.execute('''
    Use  HCMC_AI_2023
''')


# Create the new database
cursor.execute("DROP TABLE IF EXISTS scriptsTB")

# Step 3: Create a new table with the desired schema, including AUTO_INCREMENT for ID
cursor.execute('''
    CREATE TABLE scriptsTB (
        ID INT PRIMARY KEY AUTO_INCREMENT,
        video_path TEXT,
        text VARCHAR(15000),
        frame_start TEXT,
        frame_end TEXT
    )
''')

# Close the connection
conn.close()