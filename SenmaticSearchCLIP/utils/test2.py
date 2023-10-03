import csv
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
# collection_name = 'test_collection'
collection_object = database['collection_object']

result_dict = {}

# Read the CSV file and convert the result column to a dictionary
with open('resultFas_rcnn.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    
    for row in csv_reader:
        image_link = row[0]
        result_str = row[-1]
        for item in result_str.split(","):
            # Split each item by colon to separate the key and value
            # key, value = item.strip().split(":")
            # # Remove any leading or trailing whitespace from the key and value
            # key = key.strip()
            # value = int(value.strip())
            # # Add the key-value pair to the dictionary
            # result_dict[key] = value
            if (result_str is None):
                document = {
                    "image_link": image_link,
                    "result": result_str
                }
            else:
                split_item = item.strip().split(":")
                if len(split_item) == 2:
                    key, value = item.strip().split(":")
                    # Remove any leading or trailing whitespace from the key and value
                    key = key.strip()
                    value = int(value.strip())
                    # Add the key-value pair to the dictionary
                    result_dict[key] = value
            
                    document = {
                        "image_link": image_link,
                        "result": result_dict
                    }
                    collection_object.insert_one(document)
                

for doc in (collection_object).find({}):
    print(doc)

# result_str = "person: 7, traffic light: 1, chair: 2, clock: 2, tv: 2, car: 1, oven: 1, airplane: 1, train: 2, knife: 1"

# result_dict = {}

# # Split the string by comma and iterate over the resulting list
# for item in result_str.split(","):
#     # Split each item by colon to separate the key and value
#     key, value = item.strip().split(":")
#     # Remove any leading or trailing whitespace from the key and value
#     key = key.strip()
#     value = int(value.strip())
#     # Add the key-value pair to the dictionary
#     result_dict[key] = value

# print(result_dict)










# # User input
# user_input = {
#     "object": {
#         "person": "2",
#         "dog": "3",
#         "cat": "5"
#     },
#     "colors": ["red", "green", "blue"],
#     "ocr": ["Viet Nam", "Việt Nam", "Thoi su", "19000703", "19EST", "Hỗ trợ kiểm tra lỗi"]
# }

# # Create text index
# collection.create_index(
#      "$**", "text",
#     name="TextIndex",
#     default_language="none"
# )

# # Perform the search
# search_query = " ".join(user_input["object"].values()) + " " + " ".join(user_input["colors"]) + " " + " ".join(user_input["ocr"])
# search_result = collection.find(
#     {"$text": {"$search": search_query}},
#     {"score": {"$meta": "textScore"}}
# ).sort([("score", {"$meta": "textScore"})])  



# for result in search_result:
#     print(result)
# print("ok")
# client.close()

# search_query = " ".join(user_input["object"].values()) + " " + " ".join(user_input["colors"]) + " " + " ".join(user_input["ocr"])
# search_result = collection.aggregate([
#     {
#         "$match": {
#             "$text": {"$search": search_query}
#         }
#     },
#     {
#         "$project": {
#             "score": {"$meta": "textScore"},
#             "_id": 0,
#             "document": "$$ROOT"
#         }
#     },
#     {
#         "$sort": {
#             "score": {"$meta": "textScore"}
#         }
#     }
# ])