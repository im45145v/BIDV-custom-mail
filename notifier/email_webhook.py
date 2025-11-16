"""
Email webhook client for sending reports via Google Apps Script.
Enhanced with sales pitch support and attachment handling.
Posts email data to a deployed Apps Script web app.
"""
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import requests

import config

logger = logging.getLogger(__name__)


def send_email_webhook(
    to_email: str,
    subject: str,
    html_body: str,
    attachments: Optional[List[Dict[str, str]]] = None,
    customer_name: Optional[str] = None,
    segment: Optional[str] = None
) -> bool:
    """
    Send email via Google Apps Script webhook.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML email body
        attachments: Optional list of attachment dicts with 'name', 'url', 'mimeType'
        customer_name: Optional customer name for tracking
        segment: Optional customer segment for happiness tracking
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> success = send_email_webhook(
        ...     "user@example.com",
        ...     "Weekly Report",
        ...     "<h1>Hello</h1>",
        ...     [{"name": "report.pdf", "url": "https://example.com/report.pdf", "mimeType": "application/pdf"}],
        ...     "John Doe",
        ...     "vip"
        ... )
    """
    if not config.APPS_SCRIPT_WEBHOOK_URL:
        logger.warning("Apps Script webhook URL not configured")
        return False
    
    payload = {
        "to": to_email,
        "subject": subject,
        "htmlBody": html_body,
        "attachments": attachments or []
    }
    
    # Add optional tracking fields for the fun Apps Script
    if customer_name:
        payload["customerName"] = customer_name
    if segment:
        payload["segment"] = segment
    
    try:
        logger.info(f"Sending email to {to_email} with {len(attachments or [])} attachments")
        
        response = requests.post(
            config.APPS_SCRIPT_WEBHOOK_URL,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('success'):
            logger.info(f"Email sent successfully to {to_email}")
            if 'happinessLevel' in result:
                logger.info(f"  Happiness Level: {result['happinessLevel']}")
            return True
        else:
            logger.error(f"Email sending failed: {result.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook request error: {e}")
        return False
    except Exception as e:
        logger.error(f"Email sending error: {e}")
        return False


def format_customer_email(
    customer_name: str,
    customer_email: str,
    segment: str,
    kpis: Dict[str, Any],
    video_url: Optional[str] = None,
    charts_urls: Optional[List[str]] = None
) -> str:
    """
    Format HTML email body using template.
    
    Args:
        customer_name: Customer's name
        customer_email: Customer's email
        segment: Customer segment
        kpis: Dictionary of KPIs
        video_url: Optional URL to video report
        charts_urls: Optional list of chart image URLs
    
    Returns:
        Formatted HTML string
    """
    # Prepare video link
    video_link = ""
    if video_url:
        video_link = f'<a href="{video_url}" class="button">Watch Video Report</a>'
    
    # Prepare charts link
    charts_link = ""
    if charts_urls:
        charts_link = f'<a href="{charts_urls[0]}" class="button">View Charts</a>'
    
    # Format email using template
    html = config.EMAIL_TEMPLATE.format(
        name=customer_name,
        segment=segment.upper(),
        total_spend=kpis.get('total_spend', 0),
        orders_count=kpis.get('orders_count', 0),
        aov=kpis.get('average_order_value', 0),
        frequency=kpis.get('order_frequency', 0),
        top_category=kpis.get('top_category', 'N/A'),
        video_link=video_link,
        charts_link=charts_link
    )
    
    return html


def send_customer_report(
    customer_name: str,
    customer_email: str,
    segment: str,
    kpis: Dict[str, Any],
    video_url: Optional[str] = None,
    charts_urls: Optional[List[str]] = None
) -> bool:
    """
    Send complete customer report via email.
    
    Args:
        customer_name: Customer's name
        customer_email: Customer's email
        segment: Customer segment
        kpis: Dictionary of KPIs
        video_url: Optional URL to video report
        charts_urls: Optional list of chart URLs
    
    Returns:
        True if successful, False otherwise
    """
    subject = f"Your Weekly BI Report - {customer_name}"
    
    html_body = format_customer_email(
        customer_name=customer_name,
        customer_email=customer_email,
        segment=segment,
        kpis=kpis,
        video_url=video_url,
        charts_urls=charts_urls
    )
    
    return send_email_webhook(
        to_email=customer_email,
        subject=subject,
        html_body=html_body,
        attachments=charts_urls or [],
        customer_name=customer_name,
        segment=segment
    )


def send_sales_pitch_email(
    customer_name: str,
    customer_email: str,
    segment: str,
    pitch_html: str,
    subject: Optional[str] = None,
    attachment_urls: Optional[List[str]] = None
) -> bool:
    """
    Send sales pitch email with rich content and attachments.
    
    Args:
        customer_name: Customer's name
        customer_email: Customer's email
        segment: Customer segment
        pitch_html: Pre-formatted HTML pitch content
        subject: Optional custom subject line
        attachment_urls: Optional list of attachment URLs
    
    Returns:
        True if successful, False otherwise
    """
    if not subject:
        subject = f"🎁 Special Offer for {customer_name}"
    
    # Format attachments for Apps Script
    attachments = []
    if attachment_urls:
        for i, url in enumerate(attachment_urls):
            # Try to determine file type from URL
            file_ext = Path(url).suffix.lower()
            mime_types = {
                '.pdf': 'application/pdf',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.mp4': 'video/mp4',
                '.zip': 'application/zip'
            }
            mime_type = mime_types.get(file_ext, 'application/octet-stream')
            
            attachments.append({
                'name': f'attachment_{i+1}{file_ext}',
                'url': url,
                'mimeType': mime_type
            })
    
    return send_email_webhook(
        to_email=customer_email,
        subject=subject,
        html_body=pitch_html,
        attachments=attachments,
        customer_name=customer_name,
        segment=segment
    )


if __name__ == "__main__":
    # Test email formatting
    logging.basicConfig(level=logging.INFO)
    
    test_kpis = {
        'total_spend': 25000.00,
        'orders_count': 5,
        'average_order_value': 5000.00,
        'order_frequency': 2.5,
        'top_category': 'electronics'
    }
    
    html = format_customer_email(
        customer_name="John Doe",
        customer_email="john@example.com",
        segment="vip",
        kpis=test_kpis,
        video_url="https://example.com/video.mp4",
        charts_urls=["https://example.com/chart1.png"]
    )
    
    print("Email HTML preview:")
    print(html[:500] + "...")
    print("\nEmail formatting works correctly")
