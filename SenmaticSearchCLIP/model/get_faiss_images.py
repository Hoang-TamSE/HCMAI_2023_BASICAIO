import base64
import os
import cv2
import torch
import clip
import sys
from pathlib import Path

CODE_PATH = Path('D:\HCMAI_2023_BASICAIO\SenmaticSearchCLIP')

sys.path.append(str(CODE_PATH))
from model.my_faiss import Myfaiss
from model.translation import Translation
from utils.query_db import get_image_path



UPLOAD_FOLDER = "./static/data"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])        
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL, PREPROCESS = clip.load("ViT-B/32", device=DEVICE)
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "data")

DICT_IMAGE_PATH = get_image_path()
BIN_FILE=os.path.join(ROOT + "/config/faiss_normal_ViT.bin")

FAISS_TEST= Myfaiss(BIN_FILE, DICT_IMAGE_PATH, DEVICE, MODEL, Translation())


def get_response_image(id):
    image_name = DICT_IMAGE_PATH[id]
    img = cv2.imread(image_name)

    ret, jpeg = cv2.imencode('.jpg', img)
    encoded_img = base64.b64encode(jpeg).decode('ascii')
    return encoded_img


def faiss_image(query):
    encoded_images = {}
    
    text = query

    scores, idx, infos_query, images = FAISS_TEST.text_search(text, k=200)

    for id in idx:
        encoded_images[int(id)] = get_response_image(id)
    return encoded_images
