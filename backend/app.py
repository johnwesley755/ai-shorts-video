from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from generate_assets import generate_video
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # Enable CORS for your frontend app

# Output directory setup
OUTPUT_DIR = os.path.abspath("output")
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the output directory exists

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
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt is required to generate a video."}), 400
        
        # Generate the video with the prompt
        video_path = generate_video(prompt)
        video_filename = os.path.basename(video_path)

        # Ensure the file exists before serving it
        if not os.path.isfile(os.path.join(OUTPUT_DIR, video_filename)):
            return jsonify({"error": "Video generation failed"}), 500

        # Generate URLs for serving and downloading the video
        video_url = f"http://127.0.0.1:5000/output/{video_filename}"
        download_url = f"http://127.0.0.1:5000/download/{video_filename}"
        
        return jsonify({
            "videoUrl": video_url,      # For viewing the video
            "downloadUrl": download_url # For downloading the video
        })

    except Exception as e:
        app.logger.error(f"Error in /generate: {str(e)}")
        return jsonify({"error": "An unexpected error occurred during video generation."}), 500

@app.route("/output/<path:filename>")
def static_files(filename):
    """
    Serve static files from the output directory.
    """
    try:
        safe_path = os.path.abspath(os.path.join(OUTPUT_DIR, filename))
        if not safe_path.startswith(OUTPUT_DIR):
            return jsonify({"error": "Access denied"}), 403  # Prevent directory traversal attacks
        
        return send_from_directory(OUTPUT_DIR, filename)
    
    except Exception as e:
        app.logger.error(f"Error serving static file: {str(e)}")
        return jsonify({"error": "File not found"}), 404

@app.route("/download/<path:filename>")
def download_file(filename):
    """
    Serve the file as a downloadable attachment.
    """
    try:
        safe_path = os.path.abspath(os.path.join(OUTPUT_DIR, filename))
        if not safe_path.startswith(OUTPUT_DIR):
            return jsonify({"error": "Access denied"}), 403  # Prevent directory traversal attacks

        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    
    except Exception as e:
        app.logger.error(f"Error serving file for download: {str(e)}")
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    # Use dynamic port and debug flag for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
