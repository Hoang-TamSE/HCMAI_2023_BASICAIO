from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
collection_name = 'test_collection'
collection = database[collection_name]

# collection.insert_many([
#     {
#         "id": 1,
#         "path": "abc",
#         "object": {
#             "person": "1",
#             "dog": "3",
#             "cat": "5"
#         },
#         "colors": [
#             "gray",
#             "green",
#             "blue"
#         ],
#         "ocr": [
#             "Viet Nam",
#             "Việt Nam",
#             "Thoi su",
#             "19000703",
#             "19EST",
#             "Hỗ trợ kiểm tra lỗi"
#         ]
#     },
#     {
#         "id": 2,
#         "path": "aaa",
#         "object": {
#             "person": "2",
#             "dog": "3",
#             "cat": "5"
#         },
#         "colors": [
#             "red",
#             "yellow"
#         ],
#         "ocr": [
#             "Việt Nam",
#             "Thoi su",
#             "19000703",
#             "19EST",
#             "Hỗ trợ kiểm thử",
#             "Vietnam"
#         ]
#     },
#     {
#         "id": 3,
#         "path": "bbb",
#         "object": {
#             "person": "3",
#             "dog": "5",
#             "cat": "7"
#         },
#         "colors": [
#             "red",
#             "green",
#             "blue"
#         ],
#         "ocr": [
#             "Viet Nam la dat nuoc co hinh chu S",
#             "Việt Nam",
#             "Thoi su",
#             "19000703",
#             "19EST",
#             "Hỗ trợ kiểm thử"
#         ]
#     }
# ])

# collection.insert_many([
#     {
#         "id": 4,
#         "path": "abc",
#         "object": {
#             "person": "1",
#             "dog": "3",
#             "cat": "5"
#         },
#         "colors": [
#             "gray",
#             "green",
#             "blue"
#         ],
#         "ocr": [
#             "Viet Nam",
#             "Việt Nam",
#             "Thoi su",
#             "19000703",
#             "19EST",
#             "Hỗ trợ kiểm tra lỗi"
#         ]
#     },
#     {
#         "id": 5,
#         "path": "aaa",
#         "object": {
#             "person": "1",
#             "dog": "3",
#         },
#         "colors": [
#             "red",
#             "yellow"
#         ],
#         "ocr": [
#             "August",
#             "Thoi su",
#             "19000703",
#             "19EST",
#             "Hỗ trợ kiểm thử",
#             "Vietnam"
#         ]
#     },
#     {
#         "id": 6,
#         "path": "bbb",
#         "object": {
#             "person": "8",
#             "dog": "3",
#             "cat": "7"
#         },
#         "colors": [
#             "red",
#             "green",
#             "blue"
#         ],
#         "ocr": [
#             "Viet Nam la dat nuoc co hinh chu S",
#             "Việt Nam",
#             "Thoi su",
#             "19000703",
#             "19EST",
#             "Hỗ trợ kiểm thử"
#         ]
#     }
# ])

collection.create_index(
    [
        ("object", "text"),
        ("colors", "text"),
        ("ocr", "text")
    ],
    weights={
        "object": 10,
        "colors": 5,
        "ocr": 1
    },
    name="TextIndex"
)

user_input_ocr = "August Việt Nam Thoi su 19000703 19EST Hỗ trợ kiểm tra lỗi"
user_input_person = "1"
user_input_colors = ["red", "green", "blue"]

criteria = {
    "$and": [
        {
            "$text": {
                "$search": user_input_ocr
            }
        },
        {
            "object.person": user_input_person
            # "object.dog": "3"
        },
        {
            "colors": {
                "$in": user_input_colors
            }
        },
        # {
        #     "ocr": {
        #         "$in": [
        #             "Viet Nam",
        #             "Việt Nam",
        #             "Thoi su",
        #             "19000703",
        #             "19EST",
        #             "Hỗ trợ kiểm tra lỗi"
        #         ]
        #     }
        # }
    ]
}

results = collection.find(
    criteria,
    {
        "score": {
            "$meta": "textScore"
        }
    }
).sort(
    [("score", {"$meta": "textScore"})])


print("Text Search Score:")
for result in results:
    print(dict(result))

print("all doc:s")

for x in collection.find():
    print(x)

client.close()
print('okiii')