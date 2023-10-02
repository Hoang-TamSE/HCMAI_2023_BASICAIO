import mysql.connector
import os
import glob2
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "data")

connection = mysql.connector.connect(
    user='root', password='password', host='localhost'
    , port='3306', db='HCMC_AI_2023'
)

cursor = connection.cursor()

files= glob2.glob(f'{IMAGES_PATH}/*')
files.sort()

for index, row in enumerate(files):
    sql = "INSERT INTO images (ID, image_path) VALUES (%s, %s)"
    val = (index, row)
    cursor.execute(sql, val)
print("doneee")
cursor.close()
connection.commit()

