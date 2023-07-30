
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Directory to save uploaded images for OCR processing
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Use OCR.space API to process the image
        url = "https://api.ocr.space/parse/image"
        api_key = "K86447298988957"  # Replace with your API key
        with open(file_path, 'rb') as image_file:
            response = requests.post(url,
                                     files={"file": image_file},
                                     data={"apikey": api_key, "language": "eng"})
        
        # Extract text from the OCR.space API response
        result = response.json()
        if result['IsErroredOnProcessing']:
            return jsonify({"error": "Error processing the image with OCR.space API"})
        extracted_text = result['ParsedResults'][0]['ParsedText']
        return jsonify({"extracted_text": extracted_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
