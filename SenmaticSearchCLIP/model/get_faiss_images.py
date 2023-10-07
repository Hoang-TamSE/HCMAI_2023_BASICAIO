import base64
import os
import cv2
import torch
import clip
import sys
from pathlib import Path
import pandas as pd
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
CODE_PATH = Path(ROOT)

sys.path.append(str(CODE_PATH))
from model.my_faiss import Myfaiss
from model.translation import Translation
from utils.query_db import get_image_path, get_script
import csv
import json
from utils.search_frame_by_script import get_image_path_by_script
import requests



UPLOAD_FOLDER = "./static/data"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])        
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL, PREPROCESS = clip.load("ViT-L/14", device=DEVICE)

IMAGES_PATH = os.path.join(ROOT, "data")
SESSIONID = "node04x6td5z6vkoajftg3go3sp7c84"
preloaded_images = {}


DICT_IMAGE_PATH = get_image_path()

data = [{"ImageID": key, "ImagePath": value} for key, value in DICT_IMAGE_PATH.items()]

DICT_IMAGE_PATH_PD = pd.DataFrame(data)

DICT_IMAGE_PATH_PD["video_path"] = DICT_IMAGE_PATH_PD['ImagePath'].str.split("\\", expand=True).iloc[:, -1].str.split("_", n=2).apply(lambda x: '_'.join(x[:2]))
BIN_FILE=os.path.join(ROOT + "/config/faiss_normal_ViT_L14_final.bin")

FAISS_TEST= Myfaiss(BIN_FILE, DICT_IMAGE_PATH, DEVICE, MODEL, Translation(), PREPROCESS)
METADATA = {}
with open(os.path.join(ROOT, "model/metadata.json"), "r", encoding="utf-8") as file:
        METADATA = json.load(file)
def get_script_images(text):

    data = get_script(text)
    idx = []
    for row in data:
        video_path = row[1]
        start_index = row[3][:-1]
        image_path = video_path+"_"+start_index
        
            # print(image_path)
            # print(get_image_path_by_script(image_path))
        filtered_df = DICT_IMAGE_PATH_PD[DICT_IMAGE_PATH_PD['video_path'].str.contains(video_path)]
        result = filtered_df[filtered_df['ImagePath'].str.contains(image_path)]
        if result['ImageID'].empty != True: 
            idx.extend(result['ImageID'].tolist())
    print(idx)
    encoded_images = {}
    for id in idx:
        for i in range(id-5, id+5):
            encoded_images[int(i)] = get_response_image(i)
        
    return encoded_images    





def make_url(idx):
        file_name = DICT_IMAGE_PATH[int(idx)].split("\\")[-1]
        video_path = file_name.split("_")[0] + "_" + file_name.split("_")[1]
        id = file_name.split("_")[-1].split(".")[0]
        second_by_frameID = int(int(id) / 25)
        url = METADATA[video_path]
        url = url + f'&t={second_by_frameID}'
        return url

def get_near_images(id):
    encoded_images = {}


    for i in range(id-20, id + 20):
        if i >= 809694:
             break
        elif i < 0:
             break
        encoded_images[int(i)] = get_response_image(int(i))
    return encoded_images    
def get_response_image(id):
    # Check if the image is already preloaded

    image_name = DICT_IMAGE_PATH[id]
    img = cv2.imread(image_name)
    ret, jpeg = cv2.imencode('.jpg', img)
    encoded_img = base64.b64encode(jpeg).decode('ascii')

    # Encode the image
    return encoded_img

def make_csv_file(list_id):
    # with open("query.csv", 'w', newline='', encoding='utf-8') as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     for i in list_id:
    description = ""
    file_name = DICT_IMAGE_PATH[int(list_id)].split("\\")[-1]
    video_path = file_name.split("_")[0] + "_" + file_name.split("_")[1]
    id = int(file_name.split("_")[-1].split(".")[0])
    url = "https://eventretrieval.one/api/v1/submit"
    params = {
        "item": f"{video_path}",
        "frame": f"{id}",
        "session": f"{SESSIONID}",
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.ok:
        response_data = json.loads(response.text)
        description = response_data.get("description")
        status = response_data.get("status")
        # Handle the response data as needed
        print(description)
        print(status)
        print("okiiii")
    else:
        print("Request failed with status code:", response.status_code)

    return description



def faiss_image(query):
    encoded_images = {}
    
    text = query

    scores, idx, infos_query, images = FAISS_TEST.text_search(text, k=100)
    for id in idx:
        encoded_images[int(id)] = get_response_image(id)

    return encoded_images

def knn(id_image):
    encoded_images = {}
    

    scores, idx, infos_query, images = FAISS_TEST.image_search(int(id_image), k=500)

    for id in idx:
        encoded_images[int(id)] = get_response_image(id)
    return encoded_images



# get_script_images("công an")
# print(make_url(51780))
# print(DICT_IMAGE_PATH_PD)
