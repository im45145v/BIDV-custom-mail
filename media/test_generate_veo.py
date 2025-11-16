"""Quick test for Veo generation using media.veo3.generate_video_with_veo3
This script will use values from .env via python-dotenv and import the
project `config` module by adding the repo root to `sys.path` so it can be
run directly from the `media/` directory.

Run from the repo root with:
  python3 media/test_generate_veo.py
"""
import os
import sys
import logging
from pathlib import Path

# Ensure repo root is on sys.path so `import config` works when running
# this file directly from the repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Load environment from .env (if present)
try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / '.env')
except Exception:
    pass

import config
from media import veo3

logging.basicConfig(level=logging.INFO)

OUT = Path(config.OUTPUT_DIR) / "CUST0001" / "video" / "test_veo.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Short, professional 8s business presentation: clean slides with charts,\n"
    "display customer name and KPIs, modern transitions, upbeat but subtle background music."
)

print("Using VEO3 API URL:", repr(config.VEO3_API_URL))
print("Using GOOGLE_API_KEY present:", bool(config.GOOGLE_API_KEY))

res = veo3.generate_video_with_veo3(
    prompt=PROMPT,
    output_path=OUT,
    api_url=config.VEO3_API_URL or None,
    api_key=config.GOOGLE_API_KEY or None,
    options={"model": "veo-3.1-generate-preview", "aspect_ratio": "16:9", "duration": 8},
    timeout_seconds=300,
)

print("generate_video_with_veo3 returned:", res)
if res and Path(res).exists():
    print("Video saved:", res)
else:
    print("No video generated. Check logs above for errors.")
