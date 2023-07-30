
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import cv2
import numpy as np
import os

app = Flask(__name__)

# Directory to save pre-processed images
PROCESSED_IMAGE_DIR = 'processed_images'
if not os.path.exists(PROCESSED_IMAGE_DIR):
    os.makedirs(PROCESSED_IMAGE_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        image = Image.open(file.stream)
        
        # Image pre-processing using OpenCV
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        adaptive_thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((2,2), np.uint8)
        morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        scaled = cv2.resize(morphed, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        
        # Convert back to PIL Image and save for display
        processed_image = Image.fromarray(scaled)
        processed_image_path = os.path.join(PROCESSED_IMAGE_DIR, 'processed.png')
        processed_image.save(processed_image_path)
        
        # Extract text using Tesseract with specific configuration
        custom_config = r'--oem 3 --psm 6'  # Use LSTM OCR Engine and assume a uniform block of text
        text = pytesseract.image_to_string(processed_image, lang='eng', config=custom_config)
        return jsonify({"extracted_text": text, "processed_image_path": processed_image_path})

@app.route('/processed_image/<filename>')
def processed_image(filename):
    return send_from_directory(PROCESSED_IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
