from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from model.get_faiss_images import faiss_image, knn
# # from model.retrieval import get_image_list
app = Flask(__name__)

UPLOAD_FOLDER = "./static/data"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)

@app.route('/imgPath', methods=["POST"])
def get_imgPath():
    data = request.get_json()
    imgPath = data['imgPath']
    print(imgPath)
    encoded_images = []
    encoded_images = knn(query=imgPath)
    return jsonify({'data': encoded_images})

@app.route('/', methods=["POST"])
def hello():
    data = request.get_json()
    query = data['query']
    # sketch = data['sketch']
    # isEnabled = data['isEnabled']
    print(query)
    encoded_images = []
    # if isEnabled :
    #     encoded_images_faiss = faiss_image(query=query)
    #     encoded_images_sketch = get_image_list(sketch=sketch, caption=query)
    #     encoded_images.extend(encoded_images_faiss)
    #     encoded_images.extend(encoded_images_sketch)
    # else:
    encoded_images = faiss_image(query=query)
    return jsonify({'data': encoded_images})



if __name__ == "__main__":
    app.run()