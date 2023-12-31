import mysql.connector


connection = mysql.connector.connect(
    user='root', password='password', host='localhost'
    , port='3306', db='HCMC_AI_2023'
)


def get_image_path():
    DictImagePath = {}

    cur = connection.cursor()

    cur.execute("SELECT * FROM images")

    data = cur.fetchall()

    for row in data:
        DictImagePath[row[0]] = row[1]

    cur.close()

    return DictImagePath