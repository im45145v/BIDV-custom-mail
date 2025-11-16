"""
Test local MoviePy assembly using generated images and audio.
Creates `media/output/CUST0001/video/local_fallback.mp4` if images exist.
"""
import sys
from pathlib import Path
# add repo root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config
from media import video as mv

out = Path(config.OUTPUT_DIR) / 'CUST0001' / 'video' / 'local_fallback.mp4'
out.parent.mkdir(parents=True, exist_ok=True)

# Gather images from customer output (images and charts)
base = Path(config.OUTPUT_DIR) / 'CUST0001'
images = []
for sub in ('images', 'charts'):
    p = base / sub
    if p.exists():
        for f in sorted(p.iterdir()):
            if f.suffix.lower() in ('.png', '.jpg', '.jpeg'):
                images.append(f)

# Use existing audio if present
audio = None
audio_dir = base / 'audio'
if audio_dir.exists():
    # pick first mp3/m4a
    for f in audio_dir.iterdir():
        if f.suffix.lower() in ('.mp3', '.m4a', '.wav'):
            audio = f
            break

print('Found images:', images)
print('Found audio:', audio)

if not images:
    print('No images found for local assembly; aborting')
    sys.exit(1)

res = mv.create_simple_video_from_images(images, out, duration_per_image=3.0, audio_path=audio)
print('create_simple_video_from_images returned:', res)
if res and Path(res).exists():
    print('Local moviepy video saved to', res)
else:
    print('Local video assembly failed; check errors above')
