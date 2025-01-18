import os
import subprocess
from datetime import datetime
from gtts import gTTS
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

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
    return images, [False] * len(images)

pipe.safety_checker = dummy_safety_checker  # Disable the safety checker

# Initialize a text generation model
text_model_name = "google/flan-t5-large"  # Change to "gpt2" or other models if desired
text_model = AutoModelForSeq2SeqLM.from_pretrained(text_model_name)
text_tokenizer = AutoTokenizer.from_pretrained(text_model_name)

def expand_prompt(prompt):
    """Expand a prompt into a detailed description using a text generation model."""
    try:
        input_ids = text_tokenizer(prompt, return_tensors="pt").input_ids
        outputs = text_model.generate(
            input_ids,
            max_length=100,
            num_return_sequences=1,
            temperature=0.8,
            top_k=50,
            top_p=0.9
        )
        expanded_prompt = text_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return expanded_prompt
    except Exception as e:
        print(f"Error during prompt expansion: {e}")
        return prompt  # Fallback to the original prompt

def generate_video(prompt):
    """Generate a short video from a text prompt."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"generated_video_{timestamp}.mp4"
    video_path = os.path.join(OUTPUT_DIR, video_filename)

    # Step 1: Expand the prompt to generate detailed text
    expanded_prompt = expand_prompt(prompt)
    print(f"Expanded Prompt: {expanded_prompt}")

    # Step 2: Generate an image
    image_path = os.path.join(OUTPUT_DIR, f"generated_image_{timestamp}.png")
    generate_image(expanded_prompt, image_path)

    # Step 3: Add audio narration
    audio_path = os.path.join(OUTPUT_DIR, f"narration_{timestamp}.mp3")
    generate_audio(expanded_prompt, audio_path)

    # Step 4: Generate captions
    subtitle_path = os.path.join(OUTPUT_DIR, f"captions_{timestamp}.srt")
    generate_captions(expanded_prompt, subtitle_path)
    subtitle_path = subtitle_path.replace("\\", "/")  # Ensure FFmpeg-friendly paths

    # Step 5: Combine image, narration, and captions into a video using FFmpeg
    command = [
        FFMPEG_PATH, "-loop", "1", "-i", image_path, "-i", audio_path,
        "-vf", f"subtitles={subtitle_path}",  # Add subtitles to the video
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-t", "10", "-pix_fmt", "yuv420p", video_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video generated successfully at: {video_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error: {e}")
        raise RuntimeError("Failed to generate video. Check FFmpeg command and inputs.") from e

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

def generate_captions(prompt, subtitle_path):
    """Generate a simple SRT subtitle file for the expanded prompt."""
    subtitles = f"""1
00:00:00,000 --> 00:00:10,000
{prompt}
"""
    with open(subtitle_path, "w", encoding="utf-8") as f:  # Use UTF-8 encoding
        f.write(subtitles)

# Example usage
if __name__ == "__main__":
    prompt = "a tranquil forest with a stream flowing through, surrounded by lush greenery and mist"
    try:
        video_path = generate_video(prompt)
        print(f"Video generated: {video_path}")
    except Exception as e:
        print(f"Error: {e}")