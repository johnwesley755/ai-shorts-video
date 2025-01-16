import os
import subprocess
import torch
import numpy as np
from gtts import gTTS
from PIL import Image
from datetime import datetime
from pytorch_pretrained_biggan import BigGAN, truncated_noise_sample

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
    """Generate an image using BigGAN."""
    # Load the pretrained BigGAN model
    model = BigGAN.from_pretrained('biggan-deep-256')
    model.eval()

    # Map prompt to a class ID (expand this mapping for complex prompts)
    class_mapping = {
        "mountain": 970,
        "clear skies": 970,  # Same class as 'mountain' for simplicity
        "cat": 281,
        "dog": 207,
        "forest": 282,
        "beach": 978,
        "clear skies mountain": 970,  # Combined prompt
        "snow mountain": 973,         # Example of a more specific prompt
    }

    # Create a list of possible words from the prompt (split by space)
    words = prompt.lower().split()

    # Find the first matching class ID for any of the words in the prompt
    class_id = None
    for word in words:
        if word in class_mapping:
            class_id = class_mapping[word]
            break  # Use the first match

    if class_id is None:
        # If no exact match, default to 'dog' (ID 207)
        class_id = 207

    # Generate input for BigGAN
    truncation = 0.4  # Controls variability; higher = more diverse
    noise_vector = truncated_noise_sample(truncation=truncation, batch_size=1)
    noise_vector = torch.tensor(noise_vector, dtype=torch.float32)
    class_vector = torch.zeros((1, 1000), dtype=torch.float32)
    class_vector[0, class_id] = 1

    # Generate the image
    with torch.no_grad():
        output = model(noise_vector, class_vector, truncation)
    output = (output + 1) / 2  # Normalize to [0, 1]

    # Convert to an image
    output_image = output.squeeze().permute(1, 2, 0).cpu().numpy() * 255
    output_image = output_image.astype(np.uint8)
    pil_image = Image.fromarray(output_image)
    
    # Save the image
    pil_image.save(output_path)


def generate_audio(prompt, output_path):
    """Generate text-to-speech narration."""
    tts = gTTS(prompt)  # Convert text to speech
    tts.save(output_path)  # Save the audio as an MP3

# Example usage
if __name__ == "__main__":
    # Example prompt
    prompt = "mountain with clear skies"
    try:
        video_path = generate_video(prompt)
        print(f"Video generated: {video_path}")
    except RuntimeError as e:
        print(f"Error: {e}")
