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

def get_image_path_by_script(image_path):
    DictImagePath = {}

    cur = connection.cursor()

    if image_path:
        cur.execute("SELECT * FROM images WHERE image_path LIKE CONCAT('%', %s, '%')", (image_path,))
        data = cur.fetchall()
        list_path = []
        for row in data:
            if row is not None:
                return row[0]

    cur.close()
