import csv
import pandas as pd

# Read the data from the source (e.g., CSV file)
data = []
filename = "csv/resultsOCR_test - Copy.csv"
df = pd.read_csv(filename)

# for index, row in df.iterrows():
#     image_link = row['Image Path']
#     ocr_value = row['Recognized Text']
#     words = ocr_value.split()
#     odd_elements = words[1::2]
#     data.append({'image_link': image_link, 'ocr': odd_elements})

for index, row in df.iterrows():
    image_link = row['Image Path']
    ocr_value = row['Recognized Text']
    data.append({'image_link': image_link, 'ocr': ocr_value})

# Create a DataFrame
df = pd.DataFrame(data)
df.reset_index(inplace=True)
df.to_pickle('df_ocr.pkl')
print(df)
