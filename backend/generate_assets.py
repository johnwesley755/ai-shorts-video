from diffusers import StableDiffusionPipeline
from gtts import gTTS
import torch
import os
import ffmpeg

# Directory for generated outputs
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_images(prompt):
    """Generate an image from a text prompt using Stable Diffusion."""
    # Load Stable Diffusion pipeline (use GPU if available)
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Generate an image
    image = pipe(prompt).images[0]
    image_path = os.path.join(OUTPUT_DIR, "generated_image.png")
    image.save(image_path)

    return [image_path]  # Return a list of image paths

def generate_video(prompt):
    """Generate a short video from a text prompt."""
    # Step 1: Generate images
    images = generate_images(prompt)

    # Step 2: Generate narration (text-to-speech)
    tts = gTTS(prompt)
    audio_path = os.path.join(OUTPUT_DIR, "narration.mp3")
    tts.save(audio_path)

    # Step 3: Combine images and narration into a video using ffmpeg
    image_pattern = os.path.join(OUTPUT_DIR, "generated_image.png")  # You can loop or add multiple images
    video_path = os.path.join(OUTPUT_DIR, "generated_video.mp4")

    ffmpeg.input(image_pattern, framerate=1).output(video_path, audio=audio_path).run()

    return video_path
