import os
import torch
import clip
from PIL import Image
import faiss
import numpy as np

DIR_NAME = os.path.dirname(__file__)

DIR_NAME = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(DIR_NAME, os.pardir))
IMAGES_PATH = os.path.join(ROOT, "image/Keyframes_L01/keyframes")

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
features = []
for x in os.listdir(IMAGES_PATH):
  files = []
  subfolder_path = os.path.join(IMAGES_PATH, x)
    # Check if the subfolder is a directory
  if os.path.isdir(subfolder_path):
    # Loop through the files in the subfolder
        for file in os.listdir(subfolder_path):
          file= os.path.join(subfolder_path,file)
          files.append(file)
for file in files:
  image = preprocess(Image.open(file)).unsqueeze(0).to(device)
  with torch.no_grad():
      image_features = model.encode_image(image).detach().cpu().numpy()
      features.append(image_features)
image_embeddings = np.concatenate(features)

index = faiss.IndexFlatIP(image_embeddings.shape[1]) # method cosine: IndexFlatIP
index.add(image_embeddings)

a= faiss.write_index(index, os.path.join(DIR_NAME, 'faiss_normal_ViT.bin'))