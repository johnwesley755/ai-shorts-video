from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from generate_assets import generate_video
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        video_path = generate_video(prompt)
        video_url = f"http://127.0.0.1:5000/static/{os.path.basename(video_path)}"
        return jsonify({"video_url": video_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
