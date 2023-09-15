from pathlib import Path


CODE_PATH = Path('./code/')

import os
import numpy as np
import json
import torch
import sys
sys.path.append(str(CODE_PATH))
from PIL import Image
from io import BytesIO
DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = Path(os.path.join(ROOT, "images_v2"))
##make sure CODE_PATH is pointing to the correct path containing clip.py before running
from clip_2.model import convert_weights, CLIP
from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
from torch.utils.data.distributed import DistributedSampler
from dataclasses import dataclass
import json
import random
from model.translation import Translation
from langdetect import detect

from clip_2.clip import _transform, load

from clip_2.clip import tokenize

from PIL import Image, ImageDraw
model_config_file = CODE_PATH / 'training/model_configs/ViT-B-16.json'
model_file =  './model/tsbir_model_final.pt'


gpu = 0
torch.cuda.set_device(gpu)

with open(model_config_file, 'r') as f:
    model_info = json.load(f)

model = CLIP(**model_info)

loc = "cuda:{}".format(gpu)
checkpoint = torch.load(model_file, map_location=loc)

sd = checkpoint["state_dict"]
if next(iter(sd.items()))[0].startswith('module'):
    sd = {k[len('module.'):]: v for k, v in sd.items()}

model.load_state_dict(sd, strict=False)

model.eval()

model = model.cuda()


def read_json(file_name):
    with open(file_name) as handle:
        out = json.load(handle)
    return out
import os

convert_weights(model)
preprocess_train = _transform(model.visual.input_resolution, is_train=True)
preprocess_val = _transform(model.visual.input_resolution, is_train=False)
preprocess_fn = (preprocess_train, preprocess_val)


@dataclass
class DataInfo:
    dataloader: DataLoader
    sampler: DistributedSampler

class SimpleImageFolder(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __getitem__(self, index):
        image_path = self.image_paths[index]

        x = Image.open(image_path)
        if self.transform is not None:
            x = self.transform(x)
        return x, image_path



    def __len__(self):
        return len(self.image_paths)
    
image_list = []
for item in IMAGES_PATH.glob('*'):
    if '.ipynb' not in str(item):
        image_list.append(str(item))

def collate_fn(batch):
    batch = list(filter(lambda x: x is not None, batch))
    return torch.utils.data.dataloader.default_collate(batch)
dataset = SimpleImageFolder(image_list, transform=preprocess_val)
dataloader = DataLoader(
    dataset,
    batch_size=32,
    collate_fn=collate_fn,
    shuffle=False,
    num_workers=1,
    pin_memory=True,
    sampler=None,
    drop_last=False,
)
dataloader.num_samples = len(dataset)
dataloader.num_batches = len(dataloader)

data = DataInfo(dataloader, None)


cumulative_loss = 0.0
num_elements = 0.0
all_image_path = []
all_image_features = []
batch_num = 0
model = model.cuda()
with torch.no_grad():
    for batch in dataloader:

        print('Batch: ' + str(batch_num), end='')
        images, image_paths = batch
        images = images.cuda(gpu, non_blocking=True)

        image_features = model.encode_image(images)

        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        for i in image_features:
            all_image_features.append(i.cpu().numpy())
        for i in image_paths:
            all_image_path.append(i)

        batch_num += 1

        print(' -- Done\n')




def mark_boundary(img, color=(0,255,0)):
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, img.width-5, img.height-5], fill=None, outline=color, width=10)
    return img


def get_concat_hn(ims):
    sum_w = 0
    for im in ims:
        #im = im.resize((256,256))
        sum_w += 256#im.width

    max_h = 256#max([im.height for im in ims])

    dst = Image.new('RGB', (sum_w ,max_h))
    cur_x = 0
    for im in ims:
        dst.paste(im.resize((256,256)), (cur_x, 0))
        cur_x += 256#im.width
    #dst.paste(im2, (im1.width, 0))
    #dst.paste(im3, (im1.width+im2.width, 0))
    return dst

def get_feature(query_sketch, query_text):

    img1 = transformer(query_sketch).unsqueeze(0).cuda()
    txt = tokenize([str(query_text)])[0].unsqueeze(0).cuda()
    with torch.no_grad():
        sketch_feature = model.encode_sketch(img1)
        text_feature = model.encode_text(txt)
        text_feature = text_feature / text_feature.norm(dim=-1, keepdim=True)
        sketch_feature = sketch_feature / sketch_feature.norm(dim=-1, keepdim=True)

    return model.feature_fuse(sketch_feature,text_feature)

feats = all_image_features
image_paths = all_image_path
transformer = preprocess_val
model = model.cuda().eval()

from sklearn.neighbors import NearestNeighbors
nbrs = NearestNeighbors(n_neighbors=10, algorithm='brute', metric='cosine').fit(feats)

import base64
import cv2

def get_response_image(image_path):
    img = cv2.imread(image_path)

    ret, jpeg = cv2.imencode('.jpg', img)
    encoded_img = base64.b64encode(jpeg).decode('ascii')
    return encoded_img

def get_image_list(sketch, caption):
    if detect(caption) == 'vi':
            caption = Translation(caption)
    base64_image = sketch.split(",")[1]
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    sketch = image.convert("RGB")
    query_feat = get_feature(sketch, caption)

    distances, indices = nbrs.kneighbors(query_feat.cpu().numpy())

    im_list = []
    for ind in indices[0]:
        file_loc = image_paths[ind]
        im_list.append(get_response_image(file_loc))
    return im_list



