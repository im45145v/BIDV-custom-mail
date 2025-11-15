"""
Pydantic models for Customer and Order data structures.
Enhanced for personalized sales pitch generation.
"""
from datetime import date
from typing import Literal, List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Customer(BaseModel):
    """Customer data model with sales pitch personalization fields."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_id": "CUST0001",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "segment": "returning",
                "interests": ["fitness", "electronics"],
                "last_contact_date": "2024-01-15",
                "created_at": "2023-06-01",
                "engagement_score": 75,
                "preferred_contact_time": "morning",
                "pain_points": ["budget_conscious", "time_constrained"],
                "buying_behavior": "impulse_buyer",
                "response_rate": 0.65
            }
        }
    )
    
    customer_id: str = Field(..., pattern=r"^CUST\d{4}$")
    name: str
    email: EmailStr
    segment: Literal["new", "returning", "vip", "at_risk"]
    interests: List[str]
    last_contact_date: date
    created_at: date
    
    # New fields for personalized sales pitches
    engagement_score: int = Field(default=50, ge=0, le=100, description="Customer engagement level (0-100)")
    preferred_contact_time: Literal["morning", "afternoon", "evening", "weekend"] = Field(default="morning")
    pain_points: List[str] = Field(default_factory=list, description="Customer pain points for targeting")
    buying_behavior: Literal["impulse_buyer", "researcher", "bargain_hunter", "loyal", "seasonal"] = Field(default="researcher")
    response_rate: float = Field(default=0.5, ge=0, le=1, description="Historical email response rate")
    lifetime_value: Optional[float] = Field(default=None, description="Customer lifetime value in currency")


class Order(BaseModel):
    """Order data model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "order_id": "ORD00000001",
                "customer_id": "CUST0001",
                "order_date": "2024-01-10",
                "amount": 2499.99,
                "product_category": "electronics",
                "channel": "web"
            }
        }
    )
    
    order_id: str = Field(..., pattern=r"^ORD\d{8}$")
    customer_id: str = Field(..., pattern=r"^CUST\d{4}$")
    order_date: date
    amount: float = Field(..., gt=0)
    product_category: str
    channel: Literal["web", "app", "store"]
