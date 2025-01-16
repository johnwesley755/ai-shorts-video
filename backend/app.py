from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from generate_assets import generate_video
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Output directory setup
OUTPUT_DIR = os.path.abspath("output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    """
    Health check route.
    """
    return "Flask server is running. Use the `/generate` endpoint to create videos."

@app.route("/favicon.ico")
def favicon():
    """
    Handles requests for the favicon.ico to avoid unnecessary logs.
    """
    return "", 204

@app.route("/generate", methods=["POST"])
def generate():
    """
    Generate video based on a text prompt sent in the request body.
    """
    try:
        # Retrieve the prompt from the request
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required"}), 400

        prompt = data["prompt"].strip()
        if not prompt:
            return jsonify({"error": "Prompt cannot be empty"}), 400

        # Generate the video
        video_path = generate_video(prompt)
        video_filename = os.path.basename(video_path)
        
        # Ensure the file exists before sending its URL
        if not os.path.isfile(os.path.join(OUTPUT_DIR, video_filename)):
            return jsonify({"error": "Video generation failed"}), 500

        video_url = f"http://127.0.0.1:5000/output/{video_filename}"
        return jsonify({"video_url": video_url})
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Error in /generate: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/output/<path:filename>")
def static_files(filename):
    """
    Serve static files from the output directory.
    """
    try:
        safe_path = os.path.abspath(os.path.join(OUTPUT_DIR, filename))
        if not safe_path.startswith(OUTPUT_DIR):
            return jsonify({"error": "Access denied"}), 403
        return send_from_directory(OUTPUT_DIR, filename)
    except Exception as e:
        app.logger.error(f"Error serving static file: {str(e)}")
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    # Use dynamic port and debug flag for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
