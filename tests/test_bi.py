"""
Tests for BI analysis module.
"""
import pytest
import pandas as pd
from datetime import date, timedelta

from bi import analysis
from data import generator


@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    customers_df, orders_df = generator.generate_synthetic_data()
    return customers_df, orders_df


def test_calculate_customer_kpis(sample_data):
    """Test KPI calculation for a customer."""
    customers_df, orders_df = sample_data
    
    customer_id = customers_df.iloc[0]['customer_id']
    kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
    
    # Check all expected fields are present
    assert 'total_spend' in kpis
    assert 'orders_count' in kpis
    assert 'average_order_value' in kpis
    assert 'order_frequency' in kpis
    assert 'top_category' in kpis
    
    # Check types
    assert isinstance(kpis['total_spend'], float)
    assert isinstance(kpis['orders_count'], int)
    assert isinstance(kpis['average_order_value'], float)
    assert isinstance(kpis['order_frequency'], float)
    
    # Check values are reasonable
    assert kpis['total_spend'] >= 0
    assert kpis['orders_count'] >= 0
    assert kpis['average_order_value'] >= 0


def test_calculate_customer_kpis_nonexistent():
    """Test KPI calculation for non-existent customer."""
    customers_df, orders_df = generator.generate_synthetic_data()
    
    kpis = analysis.calculate_customer_kpis("CUST9999", customers_df, orders_df)
    
    # Should return zeros for non-existent customer
    assert kpis['total_spend'] == 0.0
    assert kpis['orders_count'] == 0


def test_get_customer_profile(sample_data):
    """Test getting customer profile."""
    customers_df, _ = sample_data
    
    customer_id = customers_df.iloc[0]['customer_id']
    profile = analysis.get_customer_profile(customer_id, customers_df)
    
    assert profile is not None
    assert profile['customer_id'] == customer_id
    assert 'name' in profile
    assert 'email' in profile
    assert 'segment' in profile


def test_get_customer_profile_nonexistent(sample_data):
    """Test getting non-existent customer profile."""
    customers_df, _ = sample_data
    
    profile = analysis.get_customer_profile("CUST9999", customers_df)
    
    assert profile is None


def test_get_recent_trend(sample_data):
    """Test getting recent spending trend."""
    customers_df, orders_df = sample_data
    
    customer_id = customers_df.iloc[0]['customer_id']
    trend_df = analysis.get_recent_trend(customer_id, orders_df, days=90)
    
    # Check it returns a dataframe
    assert isinstance(trend_df, pd.DataFrame)
    
    # If there's data, check columns
    if len(trend_df) > 0:
        assert 'date' in trend_df.columns
        assert 'spend' in trend_df.columns


def test_get_category_distribution(sample_data):
    """Test getting category spending distribution."""
    customers_df, orders_df = sample_data
    
    customer_id = customers_df.iloc[0]['customer_id']
    category_df = analysis.get_category_distribution(customer_id, orders_df)
    
    # Check it returns a dataframe
    assert isinstance(category_df, pd.DataFrame)
    
    # If there's data, check columns
    if len(category_df) > 0:
        assert 'category' in category_df.columns
        assert 'amount' in category_df.columns
        assert (category_df['amount'] >= 0).all()


def test_get_overall_segment_distribution(sample_data):
    """Test overall segment distribution."""
    customers_df, _ = sample_data
    
    segment_df = analysis.get_overall_segment_distribution(customers_df)
    
    assert isinstance(segment_df, pd.DataFrame)
    assert 'segment' in segment_df.columns
    assert 'count' in segment_df.columns
    assert segment_df['count'].sum() == len(customers_df)


def test_get_overall_category_share(sample_data):
    """Test overall category revenue share."""
    _, orders_df = sample_data
    
    category_df = analysis.get_overall_category_share(orders_df)
    
    assert isinstance(category_df, pd.DataFrame)
    assert 'category' in category_df.columns
    assert 'revenue' in category_df.columns
    assert (category_df['revenue'] > 0).all()


def test_get_revenue_over_time(sample_data):
    """Test revenue over time aggregation."""
    _, orders_df = sample_data
    
    revenue_df = analysis.get_revenue_over_time(orders_df, frequency='W')
    
    assert isinstance(revenue_df, pd.DataFrame)
    assert 'date' in revenue_df.columns
    assert 'revenue' in revenue_df.columns


def test_generate_summary_text():
    """Test summary text generation."""
    kpis = {
        'total_spend': 15000.00,
        'orders_count': 5,
        'average_order_value': 3000.00,
        'order_frequency': 2.5,
        'top_category': 'electronics'
    }
    
    text = analysis.generate_summary_text("John Doe", kpis)
    
    assert isinstance(text, str)
    assert "John Doe" in text
    assert "5 orders" in text
    assert "15000" in text
    assert "electronics" in text


def test_aov_calculation(sample_data):
    """Test that average order value is calculated correctly."""
    customers_df, orders_df = sample_data
    
    customer_id = customers_df.iloc[0]['customer_id']
    kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
    
    # Manually calculate AOV
    customer_orders = orders_df[orders_df['customer_id'] == customer_id]
    expected_aov = customer_orders['amount'].sum() / len(customer_orders)
    
    assert abs(kpis['average_order_value'] - expected_aov) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
