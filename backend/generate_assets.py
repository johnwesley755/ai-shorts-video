import cv2
import os
import numpy as np
from gtts import gTTS
import subprocess
from datetime import datetime

# Directory for generated outputs
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to FFmpeg (update this to your FFmpeg executable path if not in PATH)
FFMPEG_PATH = "C:\\ffmpeg\\ffmpeg.exe"

def generate_video(prompt):
    """Generate a short video from a text prompt."""
    # Generate a unique video filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"generated_video_{timestamp}.mp4"
    video_path = os.path.join(OUTPUT_DIR, video_filename)

    # Step 1: Generate an image
    image_path = os.path.join(OUTPUT_DIR, f"generated_image_{timestamp}.png")
    generate_image(prompt, image_path)

    # Check if the image was created successfully
    if not os.path.isfile(image_path):
        raise RuntimeError("Image generation failed!")

    # Step 2: Add audio narration
    audio_path = os.path.join(OUTPUT_DIR, f"narration_{timestamp}.mp3")
    generate_audio(prompt, audio_path)

    # Check if the audio was created successfully
    if not os.path.isfile(audio_path):
        raise RuntimeError("Audio generation failed!")

    # Step 3: Combine image and narration into a video using FFmpeg
    command = [
        FFMPEG_PATH, "-loop", "1", "-i", image_path, "-i", audio_path,
        "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", video_path
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e}")

    return video_path

def generate_image(prompt, output_path):
    """Generate an image with OpenCV."""
    # Create a blank black image
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    
    # Define text properties
    text = prompt[:20]  # Limit text to 20 characters
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # White text
    thickness = 2

    # Get text size to center it
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2

    # Add text to the image
    cv2.putText(img, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

    # Save the image
    cv2.imwrite(output_path, img)

def generate_audio(prompt, output_path):
    """Generate text-to-speech narration."""
    tts = gTTS(prompt)  # Convert text to speech
    tts.save(output_path)  # Save the audio as an MP3
