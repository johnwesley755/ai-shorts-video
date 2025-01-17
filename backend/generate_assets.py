import os
import subprocess
import torch
from gtts import gTTS
from datetime import datetime
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

# Directory for generated outputs
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to FFmpeg (update this to your FFmpeg executable path if not in PATH)
FFMPEG_PATH = "C:\\ffmpeg\\ffmpeg.exe"

# Initialize the StableDiffusionPipeline and set to CPU
model_id = "runwayml/stable-diffusion-v1-5"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
pipe = pipe.to("cpu")  # Set the pipeline to use CPU
pipe.enable_attention_slicing()  # Reduce memory usage

# Replace the safety checker with a dummy function (optional, for trusted use cases)
def dummy_safety_checker(images, clip_input):
    """
    Disable the safety checker by returning the images unchanged and
    marking all images as safe (False for each image).
    """
    return images, [False] * len(images)

pipe.safety_checker = dummy_safety_checker  # Disable the safety checker

def generate_video(prompt):
    """Generate a short video from a text prompt."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"generated_video_{timestamp}.mp4"
    video_path = os.path.join(OUTPUT_DIR, video_filename)

    # Step 1: Generate an image
    image_path = os.path.join(OUTPUT_DIR, f"generated_image_{timestamp}.png")
    generate_image(prompt, image_path)

    # Step 2: Add audio narration
    audio_path = os.path.join(OUTPUT_DIR, f"narration_{timestamp}.mp3")
    generate_audio(prompt, audio_path)

    # Step 3: Combine image and narration into a video using FFmpeg
    command = [
        FFMPEG_PATH, "-loop", "1", "-i", image_path, "-i", audio_path,
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-t", "10", "-pix_fmt", "yuv420p", video_path
    ]
    subprocess.run(command, check=True)

    return video_path

def generate_image(prompt, output_path):
    """Generate an image using Stable Diffusion."""
    result = pipe(prompt)
    image = result.images[0]
    image.save(output_path)

def generate_audio(prompt, output_path):
    """Generate text-to-speech narration."""
    tts = gTTS(prompt)  # Convert text to speech
    tts.save(output_path)  # Save the audio as an MP3

# Example usage
if __name__ == "__main__":
    prompt = "a serene landscape with mountains and a river at sunset"
    try:
        video_path = generate_video(prompt)
        print(f"Video generated: {video_path}")
    except Exception as e:
        print(f"Error: {e}")
