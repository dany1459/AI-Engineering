from flask import Flask, render_template, request
from flask_restful import Api
import torch
from torchvision import transforms
from model import Network, preprocess
import numpy as np

app = Flask(__name__)
api = Api(app)

model_path = 'model_mnist_digits.pth' 
model = Network()
model.load_state_dict(torch.load(model_path))
transformer = transforms.Compose([ transforms.ToTensor() ])

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def predict():
    imagefile = request.files['imagefile']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)

    threshold, _ = preprocess(image_path)
    preds = model(transformer(threshold))

    _, predicted = torch.max(preds.data, 1)

    return render_template('index.html', prediction=int(predicted[np.argmax(predicted)]))


if __name__ == "__main__":
    app.run(debug=True)
