"""
Simple video generator using OpenCV (cv2) - more reliable than MoviePy
Combines images into a video with audio
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import numpy as np
from pathlib import Path
import subprocess

def create_video_opencv(image_paths, output_path, audio_path=None, fps=24, duration_per_image=3):
    """Create video from images using OpenCV"""
    
    if not image_paths:
        print("No images provided")
        return None
    
    # Read first image to get dimensions
    first_img = cv2.imread(str(image_paths[0]))
    if first_img is None:
        print(f"Failed to read image: {image_paths[0]}")
        return None
    
    height, width = first_img.shape[:2]
    
    # Create temporary video without audio
    temp_video = output_path.parent / 'temp_video.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(temp_video), fourcc, fps, (width, height))
    
    # Add each image as frames
    for img_path in image_paths:
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Skipping invalid image: {img_path}")
            continue
        
        # Resize if needed
        if img.shape[:2] != (height, width):
            img = cv2.resize(img, (width, height))
        
        # Write frames (duration_per_image seconds per image)
        for _ in range(fps * duration_per_image):
            out.write(img)
    
    out.release()
    print(f"✓ Video created: {temp_video}")
    
    # Add audio if provided using ffmpeg
    if audio_path and audio_path.exists():
        try:
            cmd = [
                'ffmpeg', '-y', '-i', str(temp_video), '-i', str(audio_path),
                '-c:v', 'copy', '-c:a', 'aac', '-shortest', str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            temp_video.unlink()  # Remove temp file
            print(f"✓ Audio added: {output_path}")
            return output_path
        except Exception as e:
            print(f"Warning: Failed to add audio: {e}")
            # Just use video without audio
            temp_video.rename(output_path)
            return output_path
    else:
        temp_video.rename(output_path)
        return output_path

# Main test
if __name__ == '__main__':
    import config
    
    base = Path(config.OUTPUT_DIR) / 'CUST0001'
    output = base / 'video' / 'opencv_video.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    # Gather images
    images = []
    for sub in ('images', 'charts'):
        p = base / sub
        if p.exists():
            for f in sorted(p.iterdir()):
                if f.suffix.lower() in ('.png', '.jpg', '.jpeg'):
                    images.append(f)
    
    # Find audio
    audio = None
    audio_dir = base / 'audio'
    if audio_dir.exists():
        for f in audio_dir.iterdir():
            if f.suffix.lower() in ('.mp3', '.m4a', '.wav'):
                audio = f
                break
    
    print(f"Found {len(images)} images")
    print(f"Found audio: {audio}")
    
    result = create_video_opencv(images, output, audio_path=audio, duration_per_image=3)
    
    if result:
        print(f"\n✅ SUCCESS! Video saved to: {result}")
    else:
        print("\n❌ Failed to create video")
