import pandas as pd

# Read the CSV file and convert the result column to a dictionary
filename = "csv/resultsFas_rcnn_test.csv"
df = pd.read_csv(filename)

data = []

for index, row in df.iterrows():
    image_link = row['image_link']
    results = row['results']
    
    dict_objects = {}
    try:
        for object in results.split(','):
            if len(object) > 0:
                key = object.split(":")[0].strip()
                value = int(object.split(":")[1].strip())
                dict_objects[key] = value
    
        data.append({
            "image_link": image_link,
            "objects": dict_objects
        })
    except:
        data.append({
            "image_link": image_link,
            "objects": {}
        })

# Create a DataFrame
df = pd.DataFrame(data)
df.reset_index(inplace=True)

# Print the DataFrame
df.to_pickle('df_object.pkl')
print(df)

# df = pd.read_pickle('df_file.pkl')
# print(df.to_string())
