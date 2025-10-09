# Motivational Reels Generator

## Overview
🎬 A Python project to create short motivational videos with synchronized captions and voiceover.

## Requirements
- Python 3.10+
- Python libraries

🎥 [Watch the video](https://www.instagram.com/idrdev1)

## Folder Structure
```motivational-reels/
├─ scripts/
│  ├─ main.py           
│  └─ reel_generator.py 
├─ music/               
├─ Delius-Regular.ttf   
├─ requirements.txt
└─ README.md
```

## Usage
```python scripts/main.py --quote "Your motivational quote" --explanation "Explanation text"```

## Notes
- An active internet connection is required for the Pexels API and Microsoft Edge TTS.
- **Important:** Replace the `PEXELS_API_KEY` in `scripts/reel_generator.py` with your own API key from [Pexels Developers](https://www.pexels.com/api/).
- Do **not** upload your Pexels API key or any private credentials to GitHub.
- Test with short quotes first to ensure timing and captions are correct.
