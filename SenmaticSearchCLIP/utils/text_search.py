import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
collection_name = 'test_collection'
collection = database[collection_name]

# Create the text index with weights
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

# Define the search query
search_query = {
    "$or": [
        {"object": {"$regex": "1", "$options": "i"}},
        {"colors": {"$regex": "your_search_query", "$options": "i"}},
        {"ocr": {"$regex": "your_search_query", "$options": "i"}}
    ]
}

# Define the sort criteria
sort_criteria = [
    ("score", {"$meta": "textScore"}),
    ("object_score", pymongo.DESCENDING),
    ("color_score", pymongo.DESCENDING),
    ("ocr_score", pymongo.DESCENDING)
]

# Perform the find operation with search and sort
results = collection.find(search_query, {"score": {"$meta": "textScore"}}).sort(sort_criteria)

# Iterate over the sorted results
for doc in results:
    print(doc)

# Close the MongoDB connection
client.close()