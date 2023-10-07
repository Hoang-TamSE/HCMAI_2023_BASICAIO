from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from model.get_faiss_images import faiss_image, knn, make_csv_file, make_url, get_near_images,get_script_images
import csv
# # from model.retrieval import get_image_list
app = Flask(__name__)

UPLOAD_FOLDER = "./static/data"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)

@app.route('/imgPath', methods=["POST"])
def get_imgPath():
    data = request.get_json()
    imgPath = int(data['imgPath'])
    isEnabled = data['isEnabled']
    print(isEnabled)
    near_images = get_near_images(imgPath)
    knn_images = knn(imgPath)

    near_images_list = list(near_images.items())
    knn_images_list = list(knn_images.items())


    
    # print(encoded_images)
    return jsonify({'data': knn_images_list, 'minidata':near_images_list})

@app.route('/geturl', methods=["POST"])
def get_url():
    data = request.get_json()
    id = data['id']
    url = make_url(id)
    return jsonify({'data': url})

@app.route('/getbyscript', methods=["POST"])
def get_image_by_script():
    data = request.get_json()
    text = data['text']
    encoded_images = []
    print(text)
    # if isEnabled :
    #     encoded_images_faiss = faiss_image(query=query)
    #     encoded_images_sketch = get_image_list(sketch=sketch, caption=query)
    #     encoded_images.extend(encoded_images_faiss)
    #     encoded_images.extend(encoded_images_sketch)
    # else:
    encoded_images = get_script_images(text)
    encoded_images_list = list(encoded_images.items())

    return jsonify({'minidata': encoded_images_list})





@app.route('/makefile', methods=["POST"])
def make_file():
    data = request.get_json()
    imgPath = data['idx_images']
    desc = make_csv_file(imgPath)
    print(desc)
    return jsonify({'result': desc})

@app.route('/', methods=["POST"])
def hello():
    data = request.get_json()
    query = data['query']
    # sketch = data['sketch']
    # isEnabled = data['isEnabled']
    print(query)
    encoded_images = {}
    # if isEnabled :
    #     encoded_images_faiss = faiss_image(query=query)
    #     encoded_images_sketch = get_image_list(sketch=sketch, caption=query)
    #     encoded_images.extend(encoded_images_faiss)
    #     encoded_images.extend(encoded_images_sketch)
    # else:
    encoded_images = faiss_image(query=query)

    encoded_images_list = list(encoded_images.items())
    return jsonify({'data': encoded_images_list})


if __name__ == "__main__":
    app.run()