from pymongo import MongoClient

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'mydatabase'
database = client[database_name]

# Access the collection
collection_name = 'mycollection'
collection = database[collection_name]

# Retrieve the document by index (in insertion order)
index = 2
document = collection.find_one({}, skip=index)

# Print the retrieved document
print("Document at index", index, ":", document)

# Close the MongoDB connection
client.close()