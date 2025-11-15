"""
Sales pitch generation module.
Creates personalized sales pitches and recommendations based on customer patterns.
"""
from typing import Dict, Any, List
import random


def generate_sales_pitch(
    customer_name: str,
    segment: str,
    interests: List[str],
    pain_points: List[str],
    buying_behavior: str,
    engagement_score: int,
    kpis: Dict[str, Any]
) -> Dict[str, str]:
    """
    Generate a personalized sales pitch for a customer.
    
    Args:
        customer_name: Customer's name
        segment: Customer segment
        interests: List of customer interests
        pain_points: List of customer pain points
        buying_behavior: Buying behavior type
        engagement_score: Engagement score (0-100)
        kpis: Customer KPIs dictionary
    
    Returns:
        Dictionary with pitch components (subject, opening, body, cta, closing)
    """
    # Generate subject line based on segment and buying behavior
    subject = _generate_subject_line(segment, buying_behavior, interests)
    
    # Generate opening based on engagement and segment
    opening = _generate_opening(customer_name, segment, engagement_score)
    
    # Generate main pitch body
    body = _generate_pitch_body(
        segment, interests, pain_points, buying_behavior, kpis
    )
    
    # Generate call-to-action
    cta = _generate_cta(segment, buying_behavior)
    
    # Generate closing
    closing = _generate_closing(customer_name, segment)
    
    return {
        'subject': subject,
        'opening': opening,
        'body': body,
        'cta': cta,
        'closing': closing,
        'full_pitch': f"{opening}\n\n{body}\n\n{cta}\n\n{closing}"
    }


def _generate_subject_line(segment: str, buying_behavior: str, interests: List[str]) -> str:
    """Generate personalized email subject line."""
    templates = {
        'vip': [
            f"🌟 Exclusive VIP Offer: Premium {interests[0].title()} Collection",
            f"Your VIP Access: New {interests[0].title()} Arrivals",
            "🎁 Special Treat for Our Most Valued Customer",
        ],
        'returning': [
            f"Welcome Back! New {interests[0].title()} Just For You",
            f"We Missed You! Fresh {interests[0].title()} Deals Inside",
            "🎯 Handpicked Recommendations Based on Your Preferences",
        ],
        'new': [
            f"Welcome! Discover Amazing {interests[0].title()} Deals",
            f"Get Started: Your {interests[0].title()} Journey Begins",
            "👋 Welcome to the Community! Special First-Time Offer",
        ],
        'at_risk': [
            f"We Want You Back! Special {interests[0].title()} Offer",
            "🔥 Don't Miss Out: Exclusive Come-Back Deal",
            f"We've Got Something Special for You in {interests[0].title()}",
        ]
    }
    
    if segment in templates:
        return random.choice(templates[segment])
    return f"Personalized Recommendations for {interests[0].title()} Lovers"


def _generate_opening(customer_name: str, segment: str, engagement_score: int) -> str:
    """Generate personalized opening."""
    if engagement_score > 80:
        return f"Hi {customer_name}! 👋\n\nIt's always a pleasure connecting with our most engaged customers!"
    elif engagement_score > 50:
        return f"Hello {customer_name}!\n\nWe hope you're doing great! We have something exciting to share."
    elif segment == 'at_risk':
        return f"Hi {customer_name},\n\nWe noticed it's been a while since we last connected. We'd love to welcome you back with something special!"
    else:
        return f"Dear {customer_name},\n\nWe're excited to share some personalized recommendations just for you!"


def _generate_pitch_body(
    segment: str,
    interests: List[str],
    pain_points: List[str],
    buying_behavior: str,
    kpis: Dict[str, Any]
) -> str:
    """Generate main pitch body with recommendations."""
    body_parts = []
    
    # Address pain points
    if 'budget_conscious' in pain_points or 'price_sensitive' in pain_points:
        body_parts.append(
            "💰 We understand value matters to you. That's why we're offering exclusive "
            f"discounts on {interests[0]} items that match your preferences perfectly."
        )
    
    if 'time_constrained' in pain_points:
        body_parts.append(
            "⏰ Save time with our quick checkout process and express delivery options. "
            "Get what you need, when you need it."
        )
    
    if 'quality_focused' in pain_points:
        body_parts.append(
            "✨ Premium quality is our priority. Every product we recommend meets the "
            "highest standards and comes with our satisfaction guarantee."
        )
    
    # Add personalized recommendations based on interests
    body_parts.append(
        f"\n🎯 Based on your interest in {', '.join(interests[:2])}, we've curated "
        f"a selection that we think you'll love:"
    )
    
    # Add segment-specific value proposition
    if segment == 'vip':
        body_parts.append(
            "\n🌟 As a VIP customer, you get:\n"
            "• Priority access to new releases\n"
            "• Exclusive member-only pricing\n"
            "• Complimentary express shipping\n"
            "• Dedicated customer support"
        )
    elif segment == 'returning':
        body_parts.append(
            "\n💙 As a valued returning customer:\n"
            "• Special loyalty rewards points\n"
            "• Early access to sales\n"
            "• Personalized product recommendations"
        )
    elif segment == 'new':
        body_parts.append(
            "\n🎉 Welcome bonus for new members:\n"
            "• 20% off your next purchase\n"
            "• Free shipping on orders over $50\n"
            "• Access to our exclusive community"
        )
    elif segment == 'at_risk':
        body_parts.append(
            "\n💝 We want to win you back with:\n"
            "• Extra 30% discount on your favorite categories\n"
            "• No-questions-asked returns\n"
            "• Free premium membership for 3 months"
        )
    
    # Add buying behavior specific messaging
    if buying_behavior == 'impulse_buyer':
        body_parts.append(
            "\n⚡ Limited time offer! These deals won't last long. "
            "Grab them while you can!"
        )
    elif buying_behavior == 'researcher':
        body_parts.append(
            "\n📊 We've included detailed specifications and customer reviews "
            "to help you make an informed decision."
        )
    elif buying_behavior == 'bargain_hunter':
        body_parts.append(
            "\n🏷️ Hot deals alert! Save up to 50% on selected items. "
            "Best prices guaranteed!"
        )
    
    return "\n\n".join(body_parts)


def _generate_cta(segment: str, buying_behavior: str) -> str:
    """Generate call-to-action."""
    ctas = {
        'impulse_buyer': "🛒 Shop Now - Limited Stock Available!",
        'researcher': "📖 Explore Our Collection & Read Reviews",
        'bargain_hunter': "💸 See All Deals - Save Big Today!",
        'loyal': "🎁 View Your Exclusive Offers",
        'seasonal': "🌟 Check Out This Season's Must-Haves"
    }
    
    cta = ctas.get(buying_behavior, "🔍 Discover Your Perfect Match")
    
    return f"{cta}\n\n[View Personalized Recommendations] [Shop Now] [Learn More]"


def _generate_closing(customer_name: str, segment: str) -> str:
    """Generate closing message."""
    if segment == 'vip':
        return (
            f"Thank you for being an exceptional customer, {customer_name}! "
            "Your satisfaction is our top priority.\n\n"
            "Best regards,\n"
            "Your Dedicated Account Team 🌟"
        )
    elif segment == 'at_risk':
        return (
            f"We truly value your business, {customer_name}, and hope to serve you again soon.\n\n"
            "Warmly,\n"
            "The Customer Success Team 💙"
        )
    else:
        return (
            f"Happy shopping, {customer_name}! We're here if you need anything.\n\n"
            "Best wishes,\n"
            "Your Customer Care Team 😊"
        )


def generate_recommendations(
    interests: List[str],
    kpis: Dict[str, Any],
    segment: str
) -> List[Dict[str, str]]:
    """
    Generate product/service recommendations.
    
    Args:
        interests: Customer interests
        kpis: Customer KPIs
        segment: Customer segment
    
    Returns:
        List of recommendation dictionaries
    """
    recommendations = []
    
    # Generate 3-5 recommendations based on interests
    num_recommendations = random.randint(3, 5)
    
    for i, interest in enumerate(interests[:num_recommendations]):
        rec = {
            'category': interest,
            'title': f"Premium {interest.title()} Collection",
            'description': f"Handpicked {interest} items based on your preferences",
            'discount': f"{random.randint(10, 40)}% OFF",
            'urgency': random.choice([
                "Only 3 left in stock!",
                "Sale ends in 24 hours",
                "Limited edition",
                "Bestseller",
                "Trending now"
            ])
        }
        recommendations.append(rec)
    
    return recommendations


def generate_email_template_with_pitch(
    customer_name: str,
    pitch: Dict[str, str],
    recommendations: List[Dict[str, str]],
    kpis: Dict[str, Any]
) -> str:
    """
    Generate HTML email template with sales pitch.
    
    Args:
        customer_name: Customer's name
        pitch: Sales pitch dictionary
        recommendations: List of recommendations
        kpis: Customer KPIs
    
    Returns:
        HTML email template string
    """
    recommendations_html = ""
    for rec in recommendations:
        recommendations_html += f"""
        <div style="background: #fff; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #e0e0e0;">
            <h4 style="color: #0066cc; margin: 0 0 10px 0;">{rec['title']}</h4>
            <p style="margin: 5px 0;">{rec['description']}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <span style="background: #ff6b6b; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;">{rec['discount']}</span>
                <span style="color: #ff6b6b; font-size: 12px;">{rec['urgency']}</span>
            </div>
        </div>
        """
    
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 650px; margin: 0 auto; padding: 0; background: #f5f5f5; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; }}
            .content {{ padding: 30px 20px; background: #ffffff; }}
            .recommendations {{ background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 10px; }}
            .cta-button {{ display: inline-block; padding: 15px 30px; background: #0066cc; color: white; text-decoration: none; border-radius: 25px; margin: 10px 5px; font-weight: bold; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">💝 {pitch['subject']}</h1>
            </div>
            
            <div class="content">
                <div style="white-space: pre-line;">{pitch['opening']}</div>
                
                <div style="margin: 25px 0; white-space: pre-line;">{pitch['body']}</div>
                
                <div class="recommendations">
                    <h3 style="color: #333; margin-top: 0;">🎁 Your Personalized Recommendations:</h3>
                    {recommendations_html}
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" class="cta-button">🛍️ Shop Now</a>
                    <a href="#" class="cta-button" style="background: #28a745;">📱 View in App</a>
                </div>
                
                <div style="white-space: pre-line; margin-top: 30px;">{pitch['closing']}</div>
            </div>
            
            <div class="footer">
                <p>This is a personalized message based on your preferences and shopping history.</p>
                <p>&copy; 2024 AI-Powered Sales Intelligence System. All rights reserved.</p>
                <p><a href="#" style="color: #0066cc;">Unsubscribe</a> | <a href="#" style="color: #0066cc;">Manage Preferences</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return template
