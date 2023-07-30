
from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

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
        text = pytesseract.image_to_string(image)
        return jsonify({"extracted_text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
