"""
Video assembly module using MoviePy.
Combines charts, images, and audio into customer report videos.
"""
import logging
from pathlib import Path
from typing import Optional, Dict, List
from datetime import timedelta

import config

logger = logging.getLogger(__name__)


def create_text_clip(
    text: str,
    duration: float,
    size: tuple,
    fontsize: int = 60,
    color: str = 'white',
    bg_color: str = '#0066cc'
):
    """
    Create a text clip with background.
    
    Args:
        text: Text to display
        duration: Duration in seconds
        size: (width, height)
        fontsize: Font size
        color: Text color
        bg_color: Background color
    
    Returns:
        TextClip with background
    """
    from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
    
    # Create background
    bg = ColorClip(size=size, color=bg_color, duration=duration)
    
    # Create text
    txt = TextClip(
        text,
        fontsize=fontsize,
        color=color,
        size=size,
        method='caption',
        align='center'
    ).set_duration(duration)
    
    # Composite
    return CompositeVideoClip([bg, txt.set_position('center')])


def create_image_clip(
    image_path: Path,
    duration: float,
    size: tuple
):
    """
    Create an image clip resized to fit.
    
    Args:
        image_path: Path to image file
        duration: Duration in seconds
        size: (width, height)
    
    Returns:
        ImageClip
    """
    from moviepy.editor import ImageClip
    
    clip = ImageClip(str(image_path)).set_duration(duration)
    
    # Resize to fit
    clip = clip.resize(height=size[1] if clip.h > clip.w else None,
                       width=size[0] if clip.w > clip.h else None)
    
    # Center on canvas
    from moviepy.editor import CompositeVideoClip, ColorClip
    bg = ColorClip(size=size, color=(0, 0, 0), duration=duration)
    return CompositeVideoClip([bg, clip.set_position('center')])


def assemble_customer_video(
    customer_name: str,
    segment: str,
    kpis: Dict,
    charts: Dict[str, Path],
    cover_image: Optional[Path],
    audio_path: Optional[Path],
    output_path: Path
) -> Optional[Path]:
    """
    Assemble a customer report video.
    
    Args:
        customer_name: Customer's name
        segment: Customer segment
        kpis: Dictionary of KPIs
        charts: Dictionary of chart paths (spend_over_time, category_share)
        cover_image: Path to cover image (optional)
        audio_path: Path to audio narration (optional)
        output_path: Path to save video
    
    Returns:
        Path to saved video or None if failed
    
    Example:
        >>> video = assemble_customer_video(
        ...     "John Doe", "vip", kpis, charts, 
        ...     cover_image, audio, Path("output.mp4")
        ... )
    """
    try:
        from moviepy.editor import (
            VideoClip, ImageClip, AudioFileClip, 
            CompositeVideoClip, concatenate_videoclips
        )
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        size = config.VIDEO_RESOLUTION
        fps = config.VIDEO_FPS
        clips = []
        
        # Calculate durations
        if audio_path and audio_path.exists():
            audio = AudioFileClip(str(audio_path))
            audio_duration = audio.duration
            clip_duration = audio_duration / 4  # Split across 4 sections
        else:
            audio = None
            clip_duration = 4.0  # Default 4 seconds per section
        
        # 1. Intro card with name and segment
        intro_text = f"{customer_name}\nSegment: {segment.upper()}"
        try:
            intro_clip = create_text_clip(intro_text, clip_duration, size, fontsize=50)
            clips.append(intro_clip)
        except Exception as e:
            logger.warning(f"Failed to create intro clip: {e}")
        
        # 2. Cover image
        if cover_image and cover_image.exists():
            try:
                cover_clip = create_image_clip(cover_image, clip_duration, size)
                clips.append(cover_clip)
            except Exception as e:
                logger.warning(f"Failed to create cover clip: {e}")
        
        # 3. Spend over time chart
        if 'spend_over_time' in charts and charts['spend_over_time'].exists():
            try:
                spend_clip = create_image_clip(
                    charts['spend_over_time'], 
                    clip_duration, 
                    size
                )
                clips.append(spend_clip)
            except Exception as e:
                logger.warning(f"Failed to create spend chart clip: {e}")
        
        # 4. Category share chart
        if 'category_share' in charts and charts['category_share'].exists():
            try:
                category_clip = create_image_clip(
                    charts['category_share'], 
                    clip_duration, 
                    size
                )
                clips.append(category_clip)
            except Exception as e:
                logger.warning(f"Failed to create category chart clip: {e}")
        
        # If no clips, create error message
        if not clips:
            logger.error("No clips could be created")
            return None
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Add audio if available
        if audio:
            # Trim or loop audio to match video length
            if audio.duration > final_clip.duration:
                audio = audio.subclip(0, final_clip.duration)
            final_clip = final_clip.set_audio(audio)
        
        # Write video file
        final_clip.write_videofile(
            str(output_path),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(output_path.parent / 'temp_audio.m4a'),
            remove_temp=True,
            logger=None  # Suppress moviepy's verbose logging
        )
        
        # Clean up
        final_clip.close()
        if audio:
            audio.close()
        
        logger.info(f"Video assembled: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Video assembly error: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_simple_video_from_images(
    images: List[Path],
    output_path: Path,
    duration_per_image: float = 3.0,
    audio_path: Optional[Path] = None
) -> Optional[Path]:
    """
    Create a simple slideshow video from images.
    
    Args:
        images: List of image paths
        output_path: Path to save video
        duration_per_image: Duration for each image
        audio_path: Optional background audio
    
    Returns:
        Path to saved video or None if failed
    """
    try:
        from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        clips = []
        size = config.VIDEO_RESOLUTION
        
        for img_path in images:
            if img_path.exists():
                clip = create_image_clip(img_path, duration_per_image, size)
                clips.append(clip)
        
        if not clips:
            logger.error("No valid images found")
            return None
        
        final_clip = concatenate_videoclips(clips, method="compose")
        
        if audio_path and audio_path.exists():
            audio = AudioFileClip(str(audio_path))
            if audio.duration > final_clip.duration:
                audio = audio.subclip(0, final_clip.duration)
            final_clip = final_clip.set_audio(audio)
        
        final_clip.write_videofile(
            str(output_path),
            fps=config.VIDEO_FPS,
            codec='libx264',
            audio_codec='aac',
            logger=None
        )
        
        final_clip.close()
        
        logger.info(f"Simple video created: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Simple video creation error: {e}")
        return None


if __name__ == "__main__":
    # Test video creation
    logging.basicConfig(level=logging.INFO)
    
    # This is a placeholder test - actual test requires image files
    print("Video module loaded successfully")
    print("Run from Streamlit app to test with actual data")
