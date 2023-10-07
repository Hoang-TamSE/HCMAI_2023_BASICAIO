from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
collection_name = 'test_collection'
collection = database[collection_name]

# User input for keys and values
user_input = {
    "person": "10",
    "dog": "4",
    "cat": "5"
}

# Create a list to hold the conditions
conditions = []

# Build the conditions based on user input
for key, value in user_input.items():
    condition = {f"object.{key}": value}
    conditions.append(condition)

# Define the search query
search_query = {
    "$or": conditions
}

# Execute the find operation
results = collection.find(search_query)

# Iterate over the results
# for doc in results:
#     print(doc)

# Create a dictionary to store the document scores
# Create a list to store the sorted documents with scores
sorted_documents = []

# Calculate the score for each document and append it to the sorted documents
for doc in results:
    score = sum(1 for condition in conditions if doc.get("object") and all(
        doc["object"].get(key) == value for key, value in condition.items()
    ))
    doc["score"] = score
    sorted_documents.append(doc)

# Sort the documents based on the score field in descending order
sorted_documents = sorted(sorted_documents, key=lambda x: x["score"], reverse=True)

# Iterate over the sorted documents
for doc in sorted_documents:
    print(doc)

# Close the MongoDB connection
client.close()