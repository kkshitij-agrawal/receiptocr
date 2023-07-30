from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageEnhance, ImageFilter
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
        
        # Image pre-processing
        image = image.convert('L')  # Convert to grayscale
        image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Binarization
        image = image.resize((int(image.width * 2), int(image.height * 2)))  # Resize for better accuracy
        
        text = pytesseract.image_to_string(image, lang='eng')
        return jsonify({"extracted_text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
