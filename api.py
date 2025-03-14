import os
import fitz  # PyMuPDF
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API Çalışıyor! POST isteği için /summarize kullan."})

def extract_text_from_pdf(pdf_file):
    """PDF dosyasından metin çıkarır."""
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

@app.route('/summarize', methods=['POST'])
def summarize_file():
    if 'file' not in request.files:
        return jsonify({"error": "Dosya bulunamadı"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Dosya adı boş"}), 400

    text = extract_text_from_pdf(file)

    return jsonify({"summary": text[:500], "keywords": ["örnek", "PDF", "döküman"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
