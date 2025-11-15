"""
Tests for data generation module.
"""
import pytest
from datetime import date
import pandas as pd

from data import generator, schema


def test_generate_synthetic_data():
    """Test that synthetic data generation works."""
    customers_df, orders_df = generator.generate_synthetic_data()
    
    # Check dataframes are not empty
    assert len(customers_df) > 0, "Customers dataframe should not be empty"
    assert len(orders_df) > 0, "Orders dataframe should not be empty"
    
    # Check expected number of customers
    assert len(customers_df) == 25, "Should generate 25 customers"
    
    # Check customers have required columns
    assert 'customer_id' in customers_df.columns
    assert 'name' in customers_df.columns
    assert 'email' in customers_df.columns
    assert 'segment' in customers_df.columns
    assert 'interests' in customers_df.columns
    
    # Check orders have required columns
    assert 'order_id' in orders_df.columns
    assert 'customer_id' in orders_df.columns
    assert 'order_date' in orders_df.columns
    assert 'amount' in orders_df.columns
    assert 'product_category' in orders_df.columns


def test_customer_segments():
    """Test that all customer segments are valid."""
    customers_df, _ = generator.generate_synthetic_data()
    
    valid_segments = {"new", "returning", "vip", "at_risk"}
    actual_segments = set(customers_df['segment'].unique())
    
    assert actual_segments.issubset(valid_segments), \
        f"Invalid segments found: {actual_segments - valid_segments}"


def test_order_amounts_positive():
    """Test that all order amounts are positive."""
    _, orders_df = generator.generate_synthetic_data()
    
    assert (orders_df['amount'] > 0).all(), \
        "All order amounts should be positive"


def test_customer_ids_unique():
    """Test that customer IDs are unique."""
    customers_df, _ = generator.generate_synthetic_data()
    
    assert customers_df['customer_id'].is_unique, \
        "Customer IDs should be unique"


def test_order_ids_unique():
    """Test that order IDs are unique."""
    _, orders_df = generator.generate_synthetic_data()
    
    assert orders_df['order_id'].is_unique, \
        "Order IDs should be unique"


def test_customer_id_format():
    """Test customer ID format (CUST####)."""
    customers_df, _ = generator.generate_synthetic_data()
    
    for cid in customers_df['customer_id']:
        assert cid.startswith('CUST'), f"Customer ID should start with CUST: {cid}"
        assert len(cid) == 8, f"Customer ID should be 8 characters: {cid}"


def test_order_id_format():
    """Test order ID format (ORD########)."""
    _, orders_df = generator.generate_synthetic_data()
    
    for oid in orders_df['order_id']:
        assert oid.startswith('ORD'), f"Order ID should start with ORD: {oid}"
        assert len(oid) == 11, f"Order ID should be 11 characters: {oid}"


def test_orders_per_customer():
    """Test that each customer has 3-5 orders."""
    customers_df, orders_df = generator.generate_synthetic_data()
    
    for customer_id in customers_df['customer_id']:
        customer_orders = orders_df[orders_df['customer_id'] == customer_id]
        order_count = len(customer_orders)
        assert 3 <= order_count <= 5, \
            f"Customer {customer_id} should have 3-5 orders, has {order_count}"


def test_pydantic_customer_model():
    """Test that Pydantic Customer model validates correctly."""
    customer_data = {
        'customer_id': 'CUST0001',
        'name': 'John Doe',
        'email': 'john@example.com',
        'segment': 'vip',
        'interests': ['fitness', 'electronics'],
        'last_contact_date': date.today(),
        'created_at': date.today()
    }
    
    customer = schema.Customer(**customer_data)
    assert customer.customer_id == 'CUST0001'
    assert customer.segment == 'vip'


def test_pydantic_order_model():
    """Test that Pydantic Order model validates correctly."""
    order_data = {
        'order_id': 'ORD00000001',
        'customer_id': 'CUST0001',
        'order_date': date.today(),
        'amount': 2500.50,
        'product_category': 'electronics',
        'channel': 'web'
    }
    
    order = schema.Order(**order_data)
    assert order.order_id == 'ORD00000001'
    assert order.amount == 2500.50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
