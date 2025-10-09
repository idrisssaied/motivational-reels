# reel_generator.py
import asyncio
import edge_tts
import whisper
from moviepy.editor import (
    AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip
)
import os
import random, glob
import requests
import sys


PEXELS_API_KEY = "PEXELS_API_KEY"
query = "tech"
url = f"https://api.pexels.com/videos/search?query={query}&per_page=10"  # set per_page to 10

headers = {"Authorization": PEXELS_API_KEY}
response = requests.get(url, headers=headers)
data = response.json()

# Select a random video from the results
videos = data.get("videos", [])
if not videos:
    raise ValueError("❌ No videos found on Pexels")

chosen_video = random.choice(videos)
# Get the highest quality version (usually the longest one)
video_files = sorted(chosen_video["video_files"], key=lambda x: x["width"], reverse=True)
video_url = video_files[0]["link"]

print("🎬 Video URL:", video_url)

# -----------------------------
# Texts (Quote + Explanation)
# -----------------------------

# Receive values from main.py
quote = sys.argv[1]
explanation = sys.argv[2]
voc = "en-US-GuyNeural"  # Deep male voice
FONT_DEFAULT = "../Delius-Regular.ttf"

# -----------------------------
# Generate voice using Edge TTS
# -----------------------------
async def generate_voice():
    text = f"{quote}. {explanation}"
    communicate = edge_tts.Communicate(text, voc, rate="+0%", pitch="-15Hz")
    await communicate.save("voice.mp3")

asyncio.run(generate_voice())


def darken(get_frame):
    def apply_frame(t):
        frame = get_frame(t).astype("float32")
        return (frame * 0.6).astype("uint8")  # 0.6 darkens the video by 40%
    return apply_frame

# -----------------------------
# Extract word timestamps using Whisper
# -----------------------------
def transcribe_audio():
    model = whisper.load_model("base")  # use "small" or "medium" for higher accuracy
    result = model.transcribe("voice.mp3", word_timestamps=True)
    return result

def download_video(video_url, filename="temp_video.mp4"):
    print("⬇️ Downloading video...")
    r = requests.get(video_url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("✅ Video downloaded:", filename)
    return filename

# -----------------------------
# Create video with synchronized captions
# -----------------------------
def create_reel():
    # Load the voice audio
    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration

    # Load and resize background video
    local_video = download_video(video_url)
    background = VideoFileClip(local_video).resize((1080, 1920)).subclip(0, duration)
    background = background.fl_image(lambda frame: (frame * 0.3).astype("uint8")) 

    # Extract words and timestamps
    result = transcribe_audio()
    caption_clips = []

    for segment in result["segments"]:
        for word in segment["words"]:
            text = word["word"].strip()
            if not text:
                continue
            start = word["start"]
            end = word["end"]

            shadow = TextClip(
                text,
                fontsize=110,
                font=FONT_DEFAULT,
                color="black",
                size=(1000, None),
                method="caption",
                align="center"
            ).set_position(("center", "center")).set_start(start).set_duration(end - start)

            txt = TextClip(
                text,
                fontsize=100,
                font=FONT_DEFAULT,
                color="#FCB53B",
                size=(1000, None),
                method="caption",
                align="center"
            ).set_position(("center", "center")) \
             .set_start(start) \
             .set_duration(end - start)

            # Append clips directly without CompositeVideoClip
            caption_clips.append(shadow)
            caption_clips.append(txt)

    # Optional background music
    music_files = glob.glob("music/*.mp3")
    if music_files:
        music_path = random.choice(music_files)
        print("🎵 Selected background music:", music_path)
        music = AudioFileClip(music_path).volumex(0.3)
        final_audio = CompositeAudioClip([
            voice_audio.volumex(1.2),
            music.set_duration(duration).audio_fadein(2).audio_fadeout(2)
        ])
    else:
        final_audio = voice_audio

    # Merge video and captions
    final = CompositeVideoClip([background] + caption_clips)
    final = final.set_audio(final_audio)

    # Save the final video
    final.write_videofile("reel.mp4", fps=30, codec="libx264", audio_codec="aac")
    # ✅ Delete temporary video
    if os.path.exists(local_video):
        os.remove(local_video)
        print(f"🗑️ Deleted temporary video: {local_video}")

# Execute the reel creation
create_reel()
print("✅ Reel created with word-by-word synchronized captions: reel.mp4")
