import csv
import pandas as pd

# Read the data from the source (e.g., CSV file)
data = []
filename = "csv/fullColors.csv"
df = pd.read_csv(filename)

for index, row in df.iterrows():
    image_link = row['Image Path']
    colors_value = row['colors']  # Assuming the column name is 'colors'
    colors_array = [color.strip().strip(" '{}'") for color in colors_value.split(',')]
    data.append({'image_link': image_link, 'colors': colors_array})

# Create a DataFrame
df = pd.DataFrame(data)
df.reset_index(inplace=True)
df.to_pickle('df_color.pkl')
print(df)
