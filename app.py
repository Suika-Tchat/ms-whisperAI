from flask import Flask, request, jsonify
import whisper
import os
import uuid
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Chargement du modèle Whisper en dehors de la route API
model = whisper.load_model("tiny")

@app.route('/api/audio', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Vérification de la sécurité du fichier
    # filename = secure_filename(file.filename)
    # if not filename.endswith('.mp4'):
    #     return jsonify({"error": "Invalid file type"}), 400

    # Utilisation d'un fichier temporaire
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        file.save(temp_file.name)
        result = model.transcribe(temp_file.name)

    os.remove(temp_file.name)

    return jsonify({"transcription": result['text']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
