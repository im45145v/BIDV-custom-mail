"""
Email webhook client for sending reports via Google Apps Script.
Posts email data to a deployed Apps Script web app.
"""
import logging
from typing import Optional, Dict, Any, List
import requests

import config

logger = logging.getLogger(__name__)


def send_email_webhook(
    to_email: str,
    subject: str,
    html_body: str,
    attachments: Optional[List[str]] = None
) -> bool:
    """
    Send email via Google Apps Script webhook.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML email body
        attachments: Optional list of attachment URLs
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> success = send_email_webhook(
        ...     "user@example.com",
        ...     "Weekly Report",
        ...     "<h1>Hello</h1>",
        ...     ["https://example.com/report.pdf"]
        ... )
    """
    if not config.APPS_SCRIPT_WEBHOOK_URL:
        logger.warning("Apps Script webhook URL not configured")
        return False
    
    payload = {
        "to": to_email,
        "subject": subject,
        "htmlBody": html_body,
        "attachments": attachments or [],
        "secret": config.APPS_SCRIPT_WEBHOOK_SECRET
    }
    
    try:
        response = requests.post(
            config.APPS_SCRIPT_WEBHOOK_URL,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('success'):
            logger.info(f"Email sent successfully to {to_email}")
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
        video_link = f'<a href="{video_url}" class="button">📹 Watch Video Report</a>'
    
    # Prepare charts link
    charts_link = ""
    if charts_urls:
        charts_link = f'<a href="{charts_urls[0]}" class="button">📊 View Charts</a>'
    
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
        attachments=charts_urls or []
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
    print("\n✓ Email formatting works correctly")
