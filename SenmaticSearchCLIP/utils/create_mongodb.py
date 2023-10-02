from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'mydatabase'
database = client[database_name]

# Access or create a collection
collection_name = 'mycollection'
collection = database[collection_name]

# Insert documents into the collection
document1 = {"name": "John", "age": 30, "city": "New York"}
document2 = {"name": "Alice", "age": 25, "city": "London"}
document3 = {"name": "Bob", "age": 35, "city": "Paris"}

# Insert a single document and retrieve its _id
document1_id = collection.insert_one(document1).inserted_id
document2_id = collection.insert_one(document2).inserted_id
document3_id = collection.insert_one(document3).inserted_id

# Print the _id values
print("Document 1 _id:", document1_id)
print("Document 2 _id:", document2_id)
print("Document 3 _id:", document3_id)

# Close the MongoDB connection
client.close()
print('okiii')