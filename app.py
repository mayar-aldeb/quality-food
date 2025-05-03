import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index01.html")

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/assets', filename)

model = load_model("efficientnetb0_model_3classes.h5")

def read_data(image, IMG_SIZE):
    # Read and preprocess the image
    if image is None:
        print("Error reading image")
        return None

    img = cv2.resize(image, IMG_SIZE)  # Resize to fixed size
    return np.array(img)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    img = read_data(image, (224, 224))

    if img is not None:
        img = np.expand_dims(img, axis=0)
        predictions = model.predict(img)[0]  # Get predictions for 3 classes

        class_index = np.argmax(predictions)  # Get class with highest probability
        confidence = np.max(predictions) * 100  # Get confidence score

        labels = ["Fresh", "Medium", "Spoiled"]
        label = labels[class_index]

        return jsonify({"prediction": label, "confidence": float(confidence)})
    else:
        return jsonify({"error": "Failed to process image"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
