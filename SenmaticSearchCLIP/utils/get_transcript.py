from youtube_transcript_api import YouTubeTranscriptApi
import sys
from pathlib import Path
import mysql.connector

CODE_PATH = Path('D:\HCMAI_2023_BASICAIO\SenmaticSearchCLIP')

sys.path.append(str(CODE_PATH))
from utils.search_frame_by_script import get_image_path_by_script


import csv
import json

connection = mysql.connector.connect(
    user='root', password='password', host='localhost'
    , port='3306', db='HCMC_AI_2023'
)

cursor = connection.cursor()

import math 
METADATA = {}

with open("./metadata.json", "r", encoding="utf-8") as file:
        METADATA = json.load(file)

for i in    METADATA.items():
    video_path = i[0]
    id_view = i[1].split("=")[1]
    count = 0
    try:
        tx = YouTubeTranscriptApi.get_transcript(id_view, languages=['vi'])
        for i in tx:
            outtxt = (i['text']).lower()
            start_time = math.floor(i['start'])
            duration = math.floor(i['duration'])
            end_time = start_time + duration
            start_frame = "% s" % (start_time * 25)
            end_frame =  "% s" % (end_time * 25)
            if len(start_frame) < 6:
                miss_zero = "0" * (6 - len(start_frame))
                start_frame = miss_zero + start_frame
            if len(end_frame) < 6:
                miss_zero = "0" * (6 - len(end_frame))
                end_frame = miss_zero + end_frame
            print(video_path, outtxt, start_frame, end_frame)
            sql = "INSERT INTO scriptsTB (video_path, text, frame_start, frame_end) VALUES (%s, %s, %s, %s)"
            val = (video_path, outtxt, start_frame, end_frame)
            cursor.execute(sql, val)
    except:
        print(f'Video {id_view} doesn\'t have a script' )
print(count)
cursor.close()
connection.commit()

# print(list_text)

# for i in range(4200, 4325):
#     i = str(i)
#     if len(i) < 6:
#         miss_zero = "0" * (6 - len(i))
#         i = miss_zero + i
#     image_path = "L01_V001_"+i
#     print(get_image_path_by_script(image_path))

