#!/bin/bash
# Setup script for video generation with MoviePy

set -e

echo "Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y ffmpeg

echo "Installing Python packages..."
pip install --upgrade pip
pip install moviepy imageio-ffmpeg pillow numpy decorator

echo "Verifying installation..."
ffmpeg -version | head -n 1
python3 -c "import moviepy.editor as m; print('✓ MoviePy installed successfully')"
python3 -c "import imageio_ffmpeg; print('✓ imageio-ffmpeg installed successfully')"

echo ""
echo "Setup complete! You can now generate AI-powered videos."
echo "Run: python3 media/test_local_moviepy.py"
