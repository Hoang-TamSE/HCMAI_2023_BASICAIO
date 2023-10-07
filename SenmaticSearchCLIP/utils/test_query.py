from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Access or create a database
database_name = 'test_db'
database = client[database_name]

# Access or create a collection
collection_name = 'test_collection'
collection = database[collection_name]
collection.delete_many({})

collection.insert_many([
    {
        "_id": 1,
        "image_link": "D:\\AIO2023\\AIO Competition\\HCMAI_2023_BASICAIO\\SenmaticSearchCLIP\\data\\L36_V028_028045.jpg",
        "object": {
            "person": "1",
            "dog": "3",
            "cat": "5"
        },
        "color": [
            "gray",
            "green",
            "blue"
        ]
    },
    {
        "_id": 2,
        "image_link": "D:\\AIO2023\\AIO Competition\\HCMAI_2023_BASICAIO\\SenmaticSearchCLIP\\data\\L36_V028_028046.jpg",
        "object": {
            "person": "2",
            "dog": "3",
            "cat": "5"
        },
        "color": [
            "red",
            "yellow"
        ]
    },
    {
        "_id": 3,
        "image_link": "D:\\AIO2023\\AIO Competition\\HCMAI_2023_BASICAIO\\SenmaticSearchCLIP\\data\\L36_V028_028099.jpg",
        "object": {
            "person": "3",
            "dog": "5",
            "cat": "7"
        },
        "color": [
            "red",
            "green",
            "blue"
        ]
    }
])

collection.insert_many([
    {
        "_id": 4,
        "image_link": "D:\\AIO2023\\AIO Competition\\HCMAI_2023_BASICAIO\\SenmaticSearchCLIP\\data\\L36_V028_028152.jpg",
        "object": {
            "person": "1",
            "dog": "3",
            "cat": "5"
        },
        "color": [
            "gray",
            "green",
            "blue"
        ]
    },
    {
        "_id": 5,
        "image_link": "D:\\AIO2023\\AIO Competition\\HCMAI_2023_BASICAIO\\SenmaticSearchCLIP\\data\\L36_V028_028205.jpg",
        "object": {
            "person": "1",
            "dog": "3",
        },
        "color": [
            "red",
            "yellow"
        ]
    },
    {
        "_id": 6,
        "image_link": "D:\\AIO2023\\AIO Competition\\HCMAI_2023_BASICAIO\\SenmaticSearchCLIP\\data\\L36_V028_028206.jpg",
        "object": {
            "person": "8",
            "dog": "3",
            "cat": "7"
        },
        "color": [
            "red",
            "green",
            "blue"
        ]
    }
])

def search_objects_and_colors(user_input):
    # Create a list to hold the conditions for the "object" column
    object_conditions = []
    
    # Build the conditions for the "object" column based on user input
    for key, value in user_input.items():
        condition = {f"object.{key}": value}
        object_conditions.append(condition)
    
    # Create a list to hold the conditions for the "colors" column
    color_conditions = []
    
    # Build the conditions for the "color" column based on user input
    for color in user_input.get("color", []):
        condition = {"color": color}
        color_conditions.append(condition)
    
    # Combine the conditions for "object" and "colors" using "$or" operator
    search_query = {
        "$or": [
            {"$and": object_conditions},
            {"$or": color_conditions}
        ]
    }

    # Execute the find operation
    results = collection.find(search_query)
    
     # Store the image_link values in a list
    image_links = [doc["image_link"] for doc in results]
    
    return image_links

# Example usage:
user_input = {
    "person": "1",
    "color": ["red", "green"]
}

results = search_objects_and_colors(user_input)
for image_link in results:
    print(image_link)

# Close the MongoDB connection
client.close()