from flask import Flask, request, jsonify
import whisper
import os
import uuid

app = Flask(__name__)

model = whisper.load_model("tiny")

@app.route('/api/audio', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    unique_filename = str(uuid.uuid4()) + ".mp4"
    audio_path = "./" + unique_filename
    file.save(audio_path)

    result = model.transcribe(audio_path)

    os.remove(audio_path)

    return jsonify({"transcription": result['text']})

print(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)