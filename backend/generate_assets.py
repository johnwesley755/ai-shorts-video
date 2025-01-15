import cv2
import os
from gtts import gTTS
import subprocess

# Directory for generated outputs
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to FFmpeg (update this to your FFmpeg executable path if not in PATH)
FFMPEG_PATH = "C:\\ffmpeg\\ffmpeg.exe"

def generate_video(prompt):
    """Generate a short video from a text prompt."""
    # Step 1: Generate an image
    image_path = os.path.join(OUTPUT_DIR, "generated_image.png")
    generate_image(prompt, image_path)

    # Step 2: Add audio narration
    audio_path = os.path.join(OUTPUT_DIR, "narration.mp3")
    generate_audio(prompt, audio_path)

    # Step 3: Combine image and narration into a video using FFmpeg
    video_path = os.path.join(OUTPUT_DIR, "generated_video.mp4")
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
    img = cv2.putText(
        img=np.zeros((500, 500, 3), dtype=np.uint8),
        text=prompt[:20],
        org=(50, 250),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=(255, 255, 255),
        thickness=2,
        lineType=cv2.LINE_AA,
    )
    cv2.imwrite(output_path, img)

def generate_audio(prompt, output_path):
    """Generate text-to-speech narration."""
    tts = gTTS(prompt)
    tts.save(output_path)
