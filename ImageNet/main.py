import torch
from torchvision import models, transforms, datasets
from PIL import Image

from flask import Flask, request, jsonify
from io import BytesIO
import requests

PORT = 8080

app = Flask(__name__)

@app.route("/")
def hello():
    return "ImageNet Inference with AlexNet"

@app.route('/predict', methods=['GET'])
def predict():
    url = request.args['url']
    app.logger.info("Classifying image %s" % (url))

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        ])

    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)

    alexnet = models.alexnet(pretrained=True)

    alexnet.eval()

    with open('imagenet-classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]

    out = alexnet(batch_t)

    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0]
    app.logger.info("Label: %s" % (classes[index[0]]))
    app.logger.info("Confidence: %f%%" % (percentage[index[0]].item() * 100))
    return ("Label: " + classes[index[0]] + " | " + "Confidence: " + str(percentage[index[0]].item() * 100) + "%")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
