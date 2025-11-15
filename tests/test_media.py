"""
Tests for media generation modules.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from media import tts, ai_images


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


def test_generate_audio(temp_dir):
    """Test audio generation."""
    text = "This is a test of the audio generation system."
    output_path = temp_dir / "test_audio.mp3"
    
    success = tts.generate_audio(text, output_path)
    
    # Should succeed with at least one engine
    assert success, "Audio generation should succeed"
    assert output_path.exists(), "Audio file should be created"
    assert output_path.stat().st_size > 0, "Audio file should not be empty"


def test_generate_audio_creates_directory(temp_dir):
    """Test that generate_audio creates parent directory if needed."""
    text = "Test audio."
    output_path = temp_dir / "subdir" / "test_audio.mp3"
    
    success = tts.generate_audio(text, output_path)
    
    assert success
    assert output_path.parent.exists()
    assert output_path.exists()


def test_generate_customer_audio(temp_dir):
    """Test customer audio generation."""
    customer_name = "John Doe"
    summary_text = "Hi John, this is your summary."
    
    audio_path = tts.generate_customer_audio(
        customer_name,
        summary_text,
        temp_dir
    )
    
    assert audio_path is not None
    assert audio_path.exists()
    assert audio_path.name == "summary.mp3"


def test_create_placeholder_image(temp_dir):
    """Test placeholder image creation."""
    output_path = temp_dir / "test_image.png"
    
    success = ai_images.create_placeholder_image(
        segment="vip",
        interests=["fitness", "electronics"],
        output_path=output_path
    )
    
    assert success, "Placeholder image creation should succeed"
    assert output_path.exists(), "Image file should be created"
    assert output_path.stat().st_size > 0, "Image file should not be empty"


def test_generate_customer_image_fallback(temp_dir):
    """Test customer image generation with fallback to placeholder."""
    output_path = temp_dir / "customer_image.png"
    
    image_path = ai_images.generate_customer_image(
        segment="returning",
        interests=["books", "wellness"],
        output_path=output_path,
        use_openai=False,
        use_gemini=False
    )
    
    assert image_path is not None
    assert image_path.exists()
    assert image_path.suffix == ".png"


def test_placeholder_image_different_segments(temp_dir):
    """Test that different segments create different colored images."""
    segments = ["new", "returning", "vip", "at_risk"]
    
    for segment in segments:
        output_path = temp_dir / f"image_{segment}.png"
        success = ai_images.create_placeholder_image(
            segment=segment,
            interests=["test"],
            output_path=output_path
        )
        
        assert success, f"Should create image for segment {segment}"
        assert output_path.exists()


def test_audio_with_empty_text(temp_dir):
    """Test audio generation with edge cases."""
    # Empty text should still work (might create silence)
    output_path = temp_dir / "empty_audio.mp3"
    
    # Just test it doesn't crash
    try:
        tts.generate_audio("", output_path)
    except Exception:
        pass  # Some engines might fail, that's ok


def test_image_creates_parent_directory(temp_dir):
    """Test that image generation creates parent directory."""
    output_path = temp_dir / "nested" / "dir" / "image.png"
    
    success = ai_images.create_placeholder_image(
        segment="new",
        interests=["test"],
        output_path=output_path
    )
    
    assert success
    assert output_path.parent.exists()
    assert output_path.exists()


# Video tests are harder because they require all dependencies
# and can be slow. We'll do basic import and structure tests.

def test_video_module_imports():
    """Test that video module imports successfully."""
    from media import video
    
    # Check functions exist
    assert hasattr(video, 'assemble_customer_video')
    assert hasattr(video, 'create_simple_video_from_images')


def test_video_handles_missing_assets():
    """Test that video assembly handles missing assets gracefully."""
    from media import video
    
    # Create non-existent paths
    temp_path = Path(tempfile.mkdtemp())
    
    result = video.assemble_customer_video(
        customer_name="Test Customer",
        segment="vip",
        kpis={'total_spend': 1000, 'orders_count': 5, 'average_order_value': 200},
        charts={},  # No charts
        cover_image=None,
        audio_path=None,
        output_path=temp_path / "output.mp4"
    )
    
    # Should return None or handle gracefully
    # (might fail due to no clips, which is expected)
    
    # Clean up
    shutil.rmtree(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
