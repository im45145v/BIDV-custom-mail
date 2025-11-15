"""
AI image generation module with OpenAI/Gemini support and PIL fallback.
Creates cover images for video reports.
"""
import logging
from pathlib import Path
from typing import Optional, List
from PIL import Image, ImageDraw, ImageFont

import config

logger = logging.getLogger(__name__)


def generate_image_openai(prompt: str, output_path: Path) -> bool:
    """
    Generate image using OpenAI DALL-E.
    
    Args:
        prompt: Text prompt for image generation
        output_path: Path to save image
    
    Returns:
        True if successful, False otherwise
    """
    if not config.OPENAI_API_KEY:
        logger.warning("OpenAI API key not configured")
        return False
    
    try:
        from openai import OpenAI
        import requests
        
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download and save image
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        logger.info(f"Image generated with OpenAI: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"OpenAI image generation error: {e}")
        return False


def generate_image_gemini(prompt: str, output_path: Path) -> bool:
    """
    Generate image using Google Gemini.
    
    Args:
        prompt: Text prompt for image generation
        output_path: Path to save image
    
    Returns:
        True if successful, False otherwise
    """
    if not config.GOOGLE_API_KEY:
        logger.warning("Google API key not configured")
        return False
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=config.GOOGLE_API_KEY)
        
        # Note: Gemini's imagen model for image generation
        # This is a placeholder - actual implementation depends on API availability
        model = genai.GenerativeModel('gemini-pro')
        
        # Gemini primarily does text generation, not image generation yet
        # This is a placeholder for future functionality
        logger.warning("Gemini image generation not yet implemented, using fallback")
        return False
        
    except Exception as e:
        logger.error(f"Gemini image generation error: {e}")
        return False


def create_placeholder_image(
    segment: str,
    interests: List[str],
    output_path: Path
) -> bool:
    """
    Create a placeholder image using PIL.
    
    Args:
        segment: Customer segment
        interests: List of customer interests
        output_path: Path to save image
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Segment colors
        colors = {
            'new': '#4CAF50',
            'returning': '#2196F3',
            'vip': '#FFC107',
            'at_risk': '#F44336'
        }
        bg_color = colors.get(segment, '#999999')
        
        # Create image
        width, height = 1024, 1024
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font, fall back to default
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw text
        text_color = 'white'
        
        # Title
        title = "Business Intelligence"
        bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = bbox[2] - bbox[0]
        draw.text(((width - title_width) / 2, 300), title, fill=text_color, font=font_large)
        
        # Segment
        segment_text = f"Segment: {segment.upper()}"
        bbox = draw.textbbox((0, 0), segment_text, font=font_medium)
        segment_width = bbox[2] - bbox[0]
        draw.text(((width - segment_width) / 2, 400), segment_text, fill=text_color, font=font_medium)
        
        # Interests
        interests_text = f"Interests: {', '.join(interests[:3])}"
        bbox = draw.textbbox((0, 0), interests_text, font=font_small)
        interests_width = bbox[2] - bbox[0]
        draw.text(((width - interests_width) / 2, 500), interests_text, fill=text_color, font=font_small)
        
        # Draw decorative circles
        for i in range(5):
            x = (i + 1) * width // 6
            y = 700
            radius = 30
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill='white', outline=text_color, width=3)
        
        # Save image
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, 'PNG')
        
        logger.info(f"Placeholder image created: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Placeholder image creation error: {e}")
        return False


def generate_customer_image(
    segment: str,
    interests: List[str],
    output_path: Path,
    use_openai: bool = False,
    use_gemini: bool = False
) -> Optional[Path]:
    """
    Generate cover image for customer report.
    
    Tries AI generation if enabled, falls back to placeholder.
    
    Args:
        segment: Customer segment
        interests: List of customer interests
        output_path: Path to save image
        use_openai: Try OpenAI DALL-E
        use_gemini: Try Google Gemini
    
    Returns:
        Path to saved image or None if failed
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure PNG extension
    if output_path.suffix != '.png':
        output_path = output_path.with_suffix('.png')
    
    # Build prompt for AI
    prompt = config.AI_IMAGE_PROMPT_TEMPLATE.format(
        segment=segment,
        interests=", ".join(interests)
    )
    
    # Try AI generation if requested
    if use_openai:
        if generate_image_openai(prompt, output_path):
            return output_path
        logger.warning("OpenAI failed, falling back to placeholder")
    
    if use_gemini:
        if generate_image_gemini(prompt, output_path):
            return output_path
        logger.warning("Gemini failed, falling back to placeholder")
    
    # Fallback to placeholder
    if create_placeholder_image(segment, interests, output_path):
        return output_path
    
    logger.error("Failed to generate any image")
    return None


if __name__ == "__main__":
    # Test image generation
    logging.basicConfig(level=logging.INFO)
    
    test_path = Path("/tmp/test_image.png")
    result = generate_customer_image(
        segment="vip",
        interests=["fitness", "electronics", "travel"],
        output_path=test_path,
        use_openai=False,
        use_gemini=False
    )
    
    if result:
        print(f"✓ Image generated successfully: {result}")
        print(f"  File size: {result.stat().st_size} bytes")
    else:
        print("✗ Failed to generate image")
