"""
Run Veo generation using the Google GenAI SDK following the user's example.

This script reads an API key from `GEMINI_API_KEY` or `GOOGLE_API_KEY` (from
.env if present), calls `models.generate_videos`, polls for completion, and
downloads the first generated video to `media/output/CUST0001/video/veo_output.mp4`.

Requires: pip install google-genai pillow python-dotenv
"""
import os
import time
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from google import genai
from google.genai import types

# Use GEMINI_API_KEY or GOOGLE_API_KEY
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
if not API_KEY:
    raise SystemExit("No API key found in GEMINI_API_KEY or GOOGLE_API_KEY")

# Initialize client with v1beta API version required for Veo
client = genai.Client(
    api_key=API_KEY,
    http_options={'api_version': 'v1beta'}
)

MODEL = os.environ.get('VEO_MODEL') or 'veo-2.0-generate-001'

video_config = types.GenerateVideosConfig(
    aspect_ratio="16:9",
    number_of_videos=1,
    duration_seconds=8,
)

PROMPT = (
    "Short, professional 8s business presentation: clean slides with charts, "
    "display customer name and KPIs, modern transitions, subtle background music."
)

OUT = Path('media/output/CUST0001/video/veo_output.mp4')
OUT.parent.mkdir(parents=True, exist_ok=True)

def main():
    print('Using model:', MODEL)
    op = client.models.generate_videos(model=MODEL, prompt=PROMPT, config=video_config)
    print('Operation started. Polling until done...')

    start = time.time()
    timeout = 60 * 10
    while not getattr(op, 'done', False):
        if time.time() - start > timeout:
            raise RuntimeError('Video generation timed out')
        print('Polling operation status...')
        time.sleep(10)
        try:
            op = client.operations.get(op)
        except Exception:
            # Some SDK versions expect operation name
            op = client.operations.get(getattr(op, 'name', op))

    # Use result attribute (not response) for Veo operations
    result = getattr(op, 'result', None) or getattr(op, 'response', None)
    if not result:
        raise RuntimeError('Operation completed but returned no result')

    generated_videos = getattr(result, 'generated_videos', None) or getattr(result, 'generatedVideos', None)
    if not generated_videos:
        raise RuntimeError('No videos generated')

    gen = generated_videos[0]
    video_ref = getattr(gen, 'video', None)
    if not video_ref:
        raise RuntimeError('Generated video object missing video reference')

    print('Downloading generated video to', OUT)
    client.files.download(file=video_ref, output_file_path=str(OUT))
    print('Saved video to', OUT)

if __name__ == '__main__':
    main()
