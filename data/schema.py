"""
Pydantic models for Customer and Order data structures.
"""
from datetime import date
from typing import Literal, List
from pydantic import BaseModel, EmailStr, Field


class Customer(BaseModel):
    """Customer data model."""
    customer_id: str = Field(..., pattern=r"^CUST\d{4}$")
    name: str
    email: EmailStr
    segment: Literal["new", "returning", "vip", "at_risk"]
    interests: List[str]
    last_contact_date: date
    created_at: date

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST0001",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "segment": "returning",
                "interests": ["fitness", "electronics"],
                "last_contact_date": "2024-01-15",
                "created_at": "2023-06-01"
            }
        }


class Order(BaseModel):
    """Order data model."""
    order_id: str = Field(..., pattern=r"^ORD\d{8}$")
    customer_id: str = Field(..., pattern=r"^CUST\d{4}$")
    order_date: date
    amount: float = Field(..., gt=0)
    product_category: str
    channel: Literal["web", "app", "store"]

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD00000001",
                "customer_id": "CUST0001",
                "order_date": "2024-01-10",
                "amount": 2499.99,
                "product_category": "electronics",
                "channel": "web"
            }
        }
