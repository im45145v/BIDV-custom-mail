"""
Business Intelligence analysis module.
Provides KPI calculations, segmentation, and trend analysis.
"""
from typing import Dict, Any, Optional
from datetime import date, timedelta
import pandas as pd
import numpy as np


def calculate_customer_kpis(
    customer_id: str,
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Calculate KPIs for a specific customer.
    
    Args:
        customer_id: Customer ID (e.g., "CUST0001")
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    
    Returns:
        Dictionary with KPIs: total_spend, orders_count, aov, frequency, top_category
    
    Example:
        >>> kpis = calculate_customer_kpis("CUST0001", customers_df, orders_df)
        >>> kpis['total_spend']
        15499.50
    """
    # Filter orders for this customer
    customer_orders = orders_df[orders_df['customer_id'] == customer_id].copy()
    
    if len(customer_orders) == 0:
        return {
            'total_spend': 0.0,
            'orders_count': 0,
            'average_order_value': 0.0,
            'order_frequency': 0.0,
            'top_category': 'N/A',
            'days_active': 0
        }
    
    # Calculate metrics
    total_spend = customer_orders['amount'].sum()
    orders_count = len(customer_orders)
    average_order_value = total_spend / orders_count if orders_count > 0 else 0.0
    
    # Calculate order frequency (orders per month)
    if 'order_date' in customer_orders.columns:
        # Ensure order_date is datetime
        if not pd.api.types.is_datetime64_any_dtype(customer_orders['order_date']):
            customer_orders['order_date'] = pd.to_datetime(customer_orders['order_date'])
        
        date_range = (
            customer_orders['order_date'].max() - customer_orders['order_date'].min()
        )
        days_active = date_range.days + 1
        months_active = days_active / 30.0
        order_frequency = orders_count / months_active if months_active > 0 else orders_count
    else:
        days_active = 30
        order_frequency = orders_count / 1.0
    
    # Top category by spend
    category_spend = customer_orders.groupby('product_category')['amount'].sum()
    top_category = category_spend.idxmax() if len(category_spend) > 0 else 'N/A'
    
    return {
        'total_spend': float(total_spend),
        'orders_count': int(orders_count),
        'average_order_value': float(average_order_value),
        'order_frequency': float(order_frequency),
        'top_category': str(top_category),
        'days_active': int(days_active)
    }


def get_customer_profile(
    customer_id: str,
    customers_df: pd.DataFrame
) -> Optional[Dict[str, Any]]:
    """
    Get customer profile information.
    
    Args:
        customer_id: Customer ID
        customers_df: Customer dataframe
    
    Returns:
        Dictionary with customer info or None if not found
    """
    customer = customers_df[customers_df['customer_id'] == customer_id]
    
    if len(customer) == 0:
        return None
    
    return customer.iloc[0].to_dict()


def get_recent_trend(
    customer_id: str,
    orders_df: pd.DataFrame,
    days: int = 90
) -> pd.DataFrame:
    """
    Get recent spending trend for a customer.
    
    Args:
        customer_id: Customer ID
        orders_df: Orders dataframe
        days: Number of days to look back
    
    Returns:
        DataFrame with date and cumulative spend
    """
    customer_orders = orders_df[orders_df['customer_id'] == customer_id].copy()
    
    if len(customer_orders) == 0:
        return pd.DataFrame({'date': [], 'spend': []})
    
    # Ensure order_date is datetime
    if not pd.api.types.is_datetime64_any_dtype(customer_orders['order_date']):
        customer_orders['order_date'] = pd.to_datetime(customer_orders['order_date'])
    
    # Filter to recent days
    cutoff_date = pd.Timestamp(date.today() - timedelta(days=days))
    customer_orders = customer_orders[customer_orders['order_date'] >= cutoff_date]
    
    if len(customer_orders) == 0:
        return pd.DataFrame({'date': [], 'spend': []})
    
    # Sort by date and calculate cumulative spend
    customer_orders = customer_orders.sort_values('order_date')
    customer_orders['cumulative_spend'] = customer_orders['amount'].cumsum()
    
    # Return simplified dataframe
    trend_df = customer_orders[['order_date', 'cumulative_spend']].copy()
    trend_df.columns = ['date', 'spend']
    
    return trend_df


def get_category_distribution(
    customer_id: str,
    orders_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Get spending distribution by product category for a customer.
    
    Args:
        customer_id: Customer ID
        orders_df: Orders dataframe
    
    Returns:
        DataFrame with category and amount
    """
    customer_orders = orders_df[orders_df['customer_id'] == customer_id]
    
    if len(customer_orders) == 0:
        return pd.DataFrame({'category': [], 'amount': []})
    
    category_spend = customer_orders.groupby('product_category')['amount'].sum()
    category_spend = category_spend.sort_values(ascending=False)
    
    result_df = pd.DataFrame({
        'category': category_spend.index,
        'amount': category_spend.values
    })
    
    return result_df


def get_overall_segment_distribution(customers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get distribution of customers by segment.
    
    Args:
        customers_df: Customer dataframe
    
    Returns:
        DataFrame with segment and count
    """
    segment_counts = customers_df['segment'].value_counts()
    
    return pd.DataFrame({
        'segment': segment_counts.index,
        'count': segment_counts.values
    })


def get_overall_category_share(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get overall revenue share by product category.
    
    Args:
        orders_df: Orders dataframe
    
    Returns:
        DataFrame with category and revenue
    """
    category_revenue = orders_df.groupby('product_category')['amount'].sum()
    category_revenue = category_revenue.sort_values(ascending=False)
    
    return pd.DataFrame({
        'category': category_revenue.index,
        'revenue': category_revenue.values
    })


def get_revenue_over_time(
    orders_df: pd.DataFrame,
    frequency: str = 'W'
) -> pd.DataFrame:
    """
    Get revenue over time aggregated by frequency.
    
    Args:
        orders_df: Orders dataframe
        frequency: Pandas frequency string ('D', 'W', 'M', etc.)
    
    Returns:
        DataFrame with date and revenue
    """
    orders_copy = orders_df.copy()
    
    # Ensure order_date is datetime
    if not pd.api.types.is_datetime64_any_dtype(orders_copy['order_date']):
        orders_copy['order_date'] = pd.to_datetime(orders_copy['order_date'])
    
    # Group by date frequency
    orders_copy = orders_copy.set_index('order_date')
    revenue_time = orders_copy['amount'].resample(frequency).sum()
    
    # Reset index and rename columns
    result_df = revenue_time.reset_index()
    result_df.columns = ['date', 'revenue']
    
    return result_df


def generate_summary_text(
    customer_name: str,
    kpis: Dict[str, Any]
) -> str:
    """
    Generate a text summary for TTS narration.
    
    Args:
        customer_name: Customer's name
        kpis: Dictionary of KPIs
    
    Returns:
        Formatted summary text
    
    Example:
        >>> text = generate_summary_text("John Doe", kpis)
        >>> print(text)
        Hi John Doe, this is your weekly summary...
    """
    template = (
        "Hi {name}, this is your weekly summary. "
        "You placed {orders_count} orders totaling {total_spend:.0f} rupees. "
        "Your average order value is {aov:.0f} rupees. "
        "Your top category is {top_category}. "
        "Thank you for being a valued customer!"
    )
    
    return template.format(
        name=customer_name,
        orders_count=kpis['orders_count'],
        total_spend=kpis['total_spend'],
        aov=kpis['average_order_value'],
        top_category=kpis['top_category']
    )
