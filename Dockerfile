
FROM python:3.8-slim

# Install Tesseract and its dependencies
RUN apt-get update && apt-get install -y     tesseract-ocr     libtesseract-dev     libleptonica-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
