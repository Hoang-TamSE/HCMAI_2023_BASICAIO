import base64
import os
import cv2
import torch
import clip
from model.my_faiss import Myfaiss
from model.translation import Translation
from utils.query_db import get_image_path


UPLOAD_FOLDER = "./static/data"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL, PREPROCESS = clip.load("ViT-B/32", device=DEVICE)
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "image")

DICT_IMAGE_PATH = get_image_path()
BIN_FILE=os.path.join(ROOT + "/config/faiss_normal_ViT.bin")

FAISS_TEST= Myfaiss(BIN_FILE, DICT_IMAGE_PATH, DEVICE, MODEL, Translation())


def get_response_image(image_path):
    img = cv2.imread(image_path)

    ret, jpeg = cv2.imencode('.jpg', img)
    encoded_img = base64.b64encode(jpeg).decode('ascii')
    return encoded_img


def faiss_image(query):
    encoded_images = {}
    
    text = query

    scores, _, infos_query, images = FAISS_TEST.text_search(text, k=200)

    for image in images:
        encoded_images[image] = get_response_image(os.path.join(IMAGES_PATH, image))
    return encoded_images
