# main.py
import subprocess
import shlex
import argparse


def main():
    # 1. Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Create motivational reel")
    parser.add_argument("--quote", type=str, help="Motivational quote text")
    parser.add_argument("--explanation", type=str, help="Explanation for the quote")
    args = parser.parse_args()

    quote = args.quote
    explanation = args.explanation
    print("✅ Texts to use:")
    print("Quote:", quote)
    print("Explanation:", explanation)

    # 2. Run reel_generator.py with the provided texts
    cmd = f'python reel_generator.py {shlex.quote(quote)} {shlex.quote(explanation)}'
    subprocess.run(cmd, shell=True, check=True)

    # 3. After generating the video, send data to a Webhook
    payload = {
        "quote": quote,
        "explanation": explanation,
        "video_path": "reel.mp4"
    }

    print('📤 done')


if __name__ == "__main__":
    main()
