from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
collection_name = 'test_collection'
collection = database[collection_name]

# User input
user_input = {
    "object": {
        "person": "2",
        "dog": "3",
        "cat": "5"
    },
    "colors": ["red", "green", "blue"],
    "ocr": ["Viet Nam", "Việt Nam", "Thoi su", "19000703", "19EST", "Hỗ trợ kiểm tra lỗi"]
}

# Create text index
collection.create_index(
     "$**", "text",
    name="TextIndex",
    default_language="none"
)

# Perform the search
search_query = " ".join(user_input["object"].values()) + " " + " ".join(user_input["colors"]) + " " + " ".join(user_input["ocr"])
search_result = collection.find(
    {"$text": {"$search": search_query}},
    {"score": {"$meta": "textScore"}}
).sort([("score", {"$meta": "textScore"})])  

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

for result in search_result:
    print(result)
print("ok")
client.close()