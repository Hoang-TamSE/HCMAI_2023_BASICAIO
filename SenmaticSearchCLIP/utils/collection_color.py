import csv
import pandas as pd
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')


# Access or create a database
database_name = 'test_db'
database = client[database_name]


# Access or create a collection
collection_color = database['collection_color']
collection_color.delete_many({})


# Read the data from the source (e.g., CSV file)
# with open('fullColors.csv', 'r') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         image_link = row['Image Path']
#         colors_value = row['colors']  # Assuming the column name is 'colors'
#         colors_array = [color.strip().strip(" '{}'") for color in colors_value.split(',')]  # Clean up each color
       
#         # Create a new document with the 'colors' field as an array
#         document = {
#             "image_link": image_link,
#             "colors": colors_array
#         }
       
# #         # Insert the document into the MongoDB collection
#         collection_color.insert_one(document)


# for doc in (collection_color).find({}):
#     print(doc)

# print(collection_color.count_documents({}))



##############################################
# Read the data from the source (e.g., CSV file)
filename = "csv/fullColors.csv"
df = pd.read_csv(filename)

for index, row in df.iterrows():
    image_link = row['Image Path']
    colors_value = row['colors']  # Assuming the column name is 'colors'
    colors_array = [color.strip().strip(" '{}'") for color in colors_value.split(',')]  # Clean up each color
    
    # Create a new document with the 'colors' field as an array
    document = {
        "image_link": image_link,
        "colors": colors_array
    }
    
    # Insert the document into the MongoDB collection
    collection_color.insert_one(document)


for doc in (collection_color).find({}):
    print(doc)

print(collection_color.count_documents({}))

client.close()

