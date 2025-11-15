"""
Text-to-Speech module with pyttsx3 primary and gTTS fallback.
Generates audio narration for customer summaries.
"""
import logging
from pathlib import Path
from typing import Optional

import config

logger = logging.getLogger(__name__)


def generate_audio_pyttsx3(text: str, output_path: Path) -> bool:
    """
    Generate audio using pyttsx3 (offline).
    
    Args:
        text: Text to convert to speech
        output_path: Path to save audio file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', config.TTS_RATE)
        
        # Save to file
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        
        logger.info(f"Audio generated with pyttsx3: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"pyttsx3 error: {e}")
        return False


def generate_audio_gtts(text: str, output_path: Path) -> bool:
    """
    Generate audio using gTTS (requires internet).
    
    Args:
        text: Text to convert to speech
        output_path: Path to save audio file (MP3)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from gtts import gTTS
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(output_path))
        
        logger.info(f"Audio generated with gTTS: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"gTTS error: {e}")
        return False


def generate_audio(
    text: str,
    output_path: Path,
    engine: Optional[str] = None
) -> bool:
    """
    Generate audio using available TTS engine.
    
    Tries pyttsx3 first, falls back to gTTS if needed.
    
    Args:
        text: Text to convert to speech
        output_path: Path to save audio file
        engine: Optional engine preference ('pyttsx3' or 'gtts')
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> output = Path("media/output/CUST0001/audio/summary.mp3")
        >>> success = generate_audio("Hello world", output)
        >>> print(success)
        True
    """
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure output path has .mp3 extension
    if output_path.suffix != '.mp3':
        output_path = output_path.with_suffix('.mp3')
    
    # Try specified engine first
    if engine == 'gtts':
        if generate_audio_gtts(text, output_path):
            return True
        logger.warning("gTTS failed, trying pyttsx3...")
        return generate_audio_pyttsx3(text, output_path)
    
    # Default: try pyttsx3 first
    if generate_audio_pyttsx3(text, output_path):
        return True
    
    logger.warning("pyttsx3 failed, trying gTTS...")
    return generate_audio_gtts(text, output_path)


def generate_customer_audio(
    customer_name: str,
    summary_text: str,
    audio_dir: Path
) -> Optional[Path]:
    """
    Generate audio summary for a customer.
    
    Args:
        customer_name: Customer's name
        summary_text: Summary text to narrate
        audio_dir: Directory to save audio
    
    Returns:
        Path to saved audio file or None if failed
    """
    audio_dir.mkdir(parents=True, exist_ok=True)
    output_path = audio_dir / "summary.mp3"
    
    success = generate_audio(summary_text, output_path)
    
    if success:
        return output_path
    else:
        logger.error(f"Failed to generate audio for {customer_name}")
        return None


if __name__ == "__main__":
    # Test audio generation
    logging.basicConfig(level=logging.INFO)
    
    test_text = "Hi, this is a test of the text to speech system. The quick brown fox jumps over the lazy dog."
    test_path = Path("/tmp/test_audio.mp3")
    
    success = generate_audio(test_text, test_path)
    
    if success:
        print(f"✓ Audio generated successfully: {test_path}")
        print(f"  File size: {test_path.stat().st_size} bytes")
    else:
        print("✗ Failed to generate audio")
