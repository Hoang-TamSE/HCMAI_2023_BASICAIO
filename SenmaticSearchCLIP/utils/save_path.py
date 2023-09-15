import mysql.connector
import os
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "image/Keyframes_L01/keyframes")

connection = mysql.connector.connect(
    user='root', password='password', host='localhost'
    , port='3306', db='HCMC_AI_2023'
)

cursor = connection.cursor()

files=[]
for x in os.listdir(IMAGES_PATH):
  subfolder_path = os.path.join(IMAGES_PATH, x)
    # Check if the subfolder is a directory
  if os.path.isdir(subfolder_path):
    # Loop through the files in the subfolder
        for file in os.listdir(subfolder_path):
          relative_path = os.path.relpath(subfolder_path, "/home/aivn2020/HCMCAI/code/HCMAI_2023/SenmaticSearchCLIP/image")
          file= os.path.join(relative_path,file)
          files.append(file)
for index, row in enumerate(files):
    sql = "INSERT INTO images (ID, image_path) VALUES (%s, %s)"
    val = (index, row)
    cursor.execute(sql, val)
cursor.close()
connection.commit()

