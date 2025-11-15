"""
Visualization module for creating charts and graphs.
Uses matplotlib and plotly for consistent, professional charts.
"""
from typing import Optional
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


def create_spend_over_time_chart(
    trend_df: pd.DataFrame,
    customer_name: str,
    save_path: Optional[Path] = None
) -> plt.Figure:
    """
    Create a line chart showing spending over time.
    
    Args:
        trend_df: DataFrame with 'date' and 'spend' columns
        customer_name: Name for chart title
        save_path: Optional path to save the chart
    
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if len(trend_df) == 0:
        ax.text(0.5, 0.5, 'No data available', 
                ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    else:
        # Ensure date is datetime
        dates = pd.to_datetime(trend_df['date'])
        ax.plot(dates, trend_df['spend'], marker='o', 
                linewidth=2, markersize=6, color='#0066cc')
        ax.fill_between(dates, trend_df['spend'], alpha=0.3, color='#0066cc')
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cumulative Spend (₹)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}')
        )
    
    ax.set_title(f'Spending Trend - {customer_name}', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def create_category_share_chart(
    category_df: pd.DataFrame,
    customer_name: str,
    save_path: Optional[Path] = None
) -> plt.Figure:
    """
    Create a bar chart showing spending by category.
    
    Args:
        category_df: DataFrame with 'category' and 'amount' columns
        customer_name: Name for chart title
        save_path: Optional path to save the chart
    
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if len(category_df) == 0:
        ax.text(0.5, 0.5, 'No data available', 
                ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    else:
        colors = plt.cm.Set3(range(len(category_df)))
        ax.barh(category_df['category'], category_df['amount'], color=colors)
        
        ax.set_xlabel('Spend (₹)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Category', fontsize=12, fontweight='bold')
        ax.grid(True, axis='x', alpha=0.3)
        
        # Format x-axis as currency
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}')
        )
    
    ax.set_title(f'Category Spending - {customer_name}', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def create_segment_distribution_chart(
    segment_df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> plt.Figure:
    """
    Create a bar chart showing customer distribution by segment.
    
    Args:
        segment_df: DataFrame with 'segment' and 'count' columns
        save_path: Optional path to save the chart
    
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'new': '#4CAF50', 'returning': '#2196F3', 
              'vip': '#FFC107', 'at_risk': '#F44336'}
    bar_colors = [colors.get(seg, '#999999') for seg in segment_df['segment']]
    
    ax.bar(segment_df['segment'], segment_df['count'], color=bar_colors)
    
    ax.set_xlabel('Customer Segment', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
    ax.set_title('Customer Distribution by Segment', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def create_overall_category_chart(
    category_df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> plt.Figure:
    """
    Create a bar chart showing overall revenue by category.
    
    Args:
        category_df: DataFrame with 'category' and 'revenue' columns
        save_path: Optional path to save the chart
    
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = plt.cm.Set2(range(len(category_df)))
    ax.bar(category_df['category'], category_df['revenue'], color=colors)
    
    ax.set_xlabel('Product Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue (₹)', fontsize=12, fontweight='bold')
    ax.set_title('Revenue by Product Category', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}')
    )
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def create_revenue_timeline_chart(
    revenue_df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> plt.Figure:
    """
    Create a line chart showing revenue over time.
    
    Args:
        revenue_df: DataFrame with 'date' and 'revenue' columns
        save_path: Optional path to save the chart
    
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if len(revenue_df) > 0:
        dates = pd.to_datetime(revenue_df['date'])
        ax.plot(dates, revenue_df['revenue'], marker='o', 
                linewidth=2, markersize=6, color='#FF5722')
        ax.fill_between(dates, revenue_df['revenue'], alpha=0.3, color='#FF5722')
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Revenue (₹)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}')
        )
    
    ax.set_title('Revenue Over Time', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def create_plotly_spend_chart(
    trend_df: pd.DataFrame,
    customer_name: str
) -> go.Figure:
    """
    Create an interactive Plotly line chart for spending over time.
    
    Args:
        trend_df: DataFrame with 'date' and 'spend' columns
        customer_name: Name for chart title
    
    Returns:
        Plotly Figure object
    """
    if len(trend_df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(trend_df['date']),
            y=trend_df['spend'],
            mode='lines+markers',
            name='Cumulative Spend',
            line=dict(color='#0066cc', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f'Spending Trend - {customer_name}',
            xaxis_title='Date',
            yaxis_title='Cumulative Spend (₹)',
            hovermode='x unified',
            template='plotly_white'
        )
    
    return fig


def save_all_customer_charts(
    customer_id: str,
    customer_name: str,
    trend_df: pd.DataFrame,
    category_df: pd.DataFrame,
    charts_dir: Path
) -> dict:
    """
    Create and save all charts for a customer.
    
    Args:
        customer_id: Customer ID
        customer_name: Customer name
        trend_df: Spending trend data
        category_df: Category spending data
        charts_dir: Directory to save charts
    
    Returns:
        Dictionary with paths to saved charts
    """
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    saved_charts = {}
    
    # Spend over time chart
    spend_path = charts_dir / "spend_over_time.png"
    fig1 = create_spend_over_time_chart(trend_df, customer_name, spend_path)
    plt.close(fig1)
    saved_charts['spend_over_time'] = spend_path
    
    # Category share chart
    category_path = charts_dir / "category_share.png"
    fig2 = create_category_share_chart(category_df, customer_name, category_path)
    plt.close(fig2)
    saved_charts['category_share'] = category_path
    
    return saved_charts
