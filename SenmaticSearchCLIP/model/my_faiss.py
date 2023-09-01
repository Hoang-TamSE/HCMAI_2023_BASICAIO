import clip
import faiss
import numpy as np
import matplotlib.pyplot as plt
import math
from langdetect import detect




class Myfaiss:
    def __init__(self, bin_file : str,id2img_fps, device, model, translater):
        self.index= self.load_bin_file(bin_file)
        self.id2img_fps= id2img_fps
        self.device= device
        self.model= model
        self.bin_file = bin_file
        self.translater = translater
    
    def load_bin_file(self, bin_file: str):
        return faiss.read_index(bin_file)
    
    def show_images(self, image_paths):
        fig = plt.figure(figsize=(15, 10))
        columns = int(math.sqrt(len(image_paths)))
        rows = int(np.ceil(len(image_paths)/columns))

        for i in range(1, columns*rows +1):
          img = plt.imread(image_paths[i - 1])
          ax = fig.add_subplot(rows, columns, i)
          ax.set_title('/'.join(image_paths[i - 1].split('/')[-3:]))

          plt.imshow(img)
          plt.axis("off")

        plt.show()
        
    def image_search( self,id_query, k, bin_file): 
        
        query_feats = self.index.reconstruct(id_query).reshape(1,-1)

        scores, idx_image = self.index.search(query_feats, k=k)
        idx_image = idx_image.flatten()

        infos_query = list(map(self.id2img_fps.get, list(idx_image)))
        image_paths = [info for info in infos_query]

        
        return scores, idx_image, infos_query, image_paths
    def text_search(self, text, k):
        if detect(text) == 'vi':
            text = self.translater(text)

        ###### TEXT FEATURES EXACTING ######
        text = clip.tokenize([text]).to(self.device)  
        text_features = self.model.encode_text(text).cpu().detach().numpy().astype(np.float32)

        ###### SEARCHING #####
        scores, idx_image = self.index.search(text_features, k=k)
        idx_image = idx_image.flatten()

        ###### GET INFOS KEYFRAMES_ID ######
        infos_query = list(map(self.id2img_fps.get, list(idx_image)))
        image_paths = [info for info in infos_query]

        return scores, idx_image, infos_query, image_paths