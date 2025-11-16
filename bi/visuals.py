"""
Visualization module for creating charts and graphs.
Uses matplotlib and plotly for consistent, professional charts.
Enhanced with advanced visualization types for comprehensive analytics.
"""
from typing import Optional, Dict, Any
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


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


def create_engagement_heatmap(
    customers_df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Create a heatmap showing engagement scores by segment and buying behavior.
    
    Args:
        customers_df: Customer dataframe
        save_path: Optional path to save the chart
    
    Returns:
        Plotly Figure object
    """
    # Pivot data for heatmap
    if 'engagement_score' in customers_df.columns and 'buying_behavior' in customers_df.columns:
        pivot_data = customers_df.pivot_table(
            values='engagement_score',
            index='segment',
            columns='buying_behavior',
            aggfunc='mean'
        )
    else:
        # Return empty figure if columns don't exist
        fig = go.Figure()
        fig.add_annotation(
            text="Engagement data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        text=pivot_data.values.round(1),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Avg Engagement Score")
    ))
    
    fig.update_layout(
        title='Customer Engagement Heatmap by Segment & Behavior',
        xaxis_title='Buying Behavior',
        yaxis_title='Customer Segment',
        height=500
    )
    
    if save_path:
        fig.write_image(str(save_path))
    
    return fig


def create_funnel_chart(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a funnel chart showing customer journey stages.
    
    Args:
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    # Calculate funnel metrics
    total_customers = len(customers_df)
    active_customers = customers_df[customers_df['segment'] != 'at_risk'].shape[0]
    returning_plus = customers_df[customers_df['segment'].isin(['returning', 'vip'])].shape[0]
    vip_customers = customers_df[customers_df['segment'] == 'vip'].shape[0]
    
    fig = go.Figure(go.Funnel(
        y=['All Customers', 'Active', 'Returning+', 'VIP'],
        x=[total_customers, active_customers, returning_plus, vip_customers],
        textinfo="value+percent initial",
        marker=dict(color=['#2196F3', '#4CAF50', '#FF9800', '#FFC107'])
    ))
    
    fig.update_layout(
        title='Customer Journey Funnel',
        height=500
    )
    
    return fig


def create_cohort_retention_chart(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a cohort retention analysis chart.
    
    Args:
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    # Simplified retention: customers with orders in different months
    orders_copy = orders_df.copy()
    orders_copy['order_date'] = pd.to_datetime(orders_copy['order_date'])
    orders_copy['month'] = orders_copy['order_date'].dt.to_period('M')
    
    # Count unique customers per month
    monthly_customers = orders_copy.groupby('month')['customer_id'].nunique()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(m) for m in monthly_customers.index],
        y=monthly_customers.values,
        marker_color='#0066cc',
        name='Active Customers'
    ))
    
    fig.update_layout(
        title='Monthly Active Customers (Retention Proxy)',
        xaxis_title='Month',
        yaxis_title='Number of Active Customers',
        height=400
    )
    
    return fig


def create_ltv_distribution(
    customers_df: pd.DataFrame
) -> go.Figure:
    """
    Create a distribution chart for customer lifetime value.
    
    Args:
        customers_df: Customer dataframe
    
    Returns:
        Plotly Figure object
    """
    if 'lifetime_value' not in customers_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Lifetime value data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = px.histogram(
        customers_df,
        x='lifetime_value',
        color='segment',
        nbins=30,
        title='Customer Lifetime Value Distribution by Segment',
        labels={'lifetime_value': 'Lifetime Value (₹)', 'count': 'Number of Customers'},
        color_discrete_map={
            'new': '#4CAF50',
            'returning': '#2196F3',
            'vip': '#FFC107',
            'at_risk': '#F44336'
        }
    )
    
    fig.update_layout(height=500)
    
    return fig


def create_segment_comparison_chart(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a radar chart comparing segments across multiple metrics.
    
    Args:
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    # Calculate metrics by segment
    segment_metrics = []
    
    for segment in ['new', 'returning', 'vip', 'at_risk']:
        seg_customers = customers_df[customers_df['segment'] == segment]
        seg_orders = orders_df[orders_df['customer_id'].isin(seg_customers['customer_id'])]
        
        metrics = {
            'segment': segment,
            'avg_order_value': seg_orders['amount'].mean() if len(seg_orders) > 0 else 0,
            'total_orders': len(seg_orders),
            'avg_engagement': seg_customers['engagement_score'].mean() if 'engagement_score' in seg_customers else 50,
            'response_rate': seg_customers['response_rate'].mean() if 'response_rate' in seg_customers else 0.5,
            'customer_count': len(seg_customers)
        }
        segment_metrics.append(metrics)
    
    # Normalize metrics to 0-100 scale for radar chart
    metrics_df = pd.DataFrame(segment_metrics)
    
    fig = go.Figure()
    
    colors = {'new': '#4CAF50', 'returning': '#2196F3', 
              'vip': '#FFC107', 'at_risk': '#F44336'}
    
    for _, row in metrics_df.iterrows():
        # Normalize each metric to 0-100 scale
        normalized = [
            (row['avg_order_value'] / metrics_df['avg_order_value'].max() * 100) if metrics_df['avg_order_value'].max() > 0 else 0,
            (row['total_orders'] / metrics_df['total_orders'].max() * 100) if metrics_df['total_orders'].max() > 0 else 0,
            row['avg_engagement'],
            row['response_rate'] * 100,
            (row['customer_count'] / metrics_df['customer_count'].max() * 100) if metrics_df['customer_count'].max() > 0 else 0
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=normalized,
            theta=['Avg Order Value', 'Total Orders', 'Engagement', 'Response Rate', 'Customer Count'],
            fill='toself',
            name=row['segment'].upper(),
            line_color=colors.get(row['segment'], '#999999')
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title='Segment Performance Comparison (Normalized)',
        height=600
    )
    
    return fig


def create_monthly_trend_comparison(
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a line chart comparing revenue trends month-over-month.
    
    Args:
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    orders_copy = orders_df.copy()
    orders_copy['order_date'] = pd.to_datetime(orders_copy['order_date'])
    orders_copy['month'] = orders_copy['order_date'].dt.to_period('M')
    orders_copy['year'] = orders_copy['order_date'].dt.year
    
    monthly_revenue = orders_copy.groupby(['year', 'month'])['amount'].sum().reset_index()
    monthly_revenue['month_str'] = monthly_revenue['month'].astype(str)
    
    fig = go.Figure()
    
    for year in monthly_revenue['year'].unique():
        year_data = monthly_revenue[monthly_revenue['year'] == year]
        fig.add_trace(go.Scatter(
            x=year_data['month_str'],
            y=year_data['amount'],
            mode='lines+markers',
            name=f'Year {year}',
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title='Revenue Trends: Month-over-Month Comparison',
        xaxis_title='Month',
        yaxis_title='Revenue (₹)',
        height=500,
        hovermode='x unified'
    )
    
    return fig


def create_customer_value_scatter(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a scatter plot showing customer engagement vs lifetime value.
    
    Args:
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    if 'lifetime_value' not in customers_df.columns or 'engagement_score' not in customers_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Required data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = px.scatter(
        customers_df,
        x='engagement_score',
        y='lifetime_value',
        color='segment',
        size='lifetime_value',
        hover_data=['name', 'segment', 'buying_behavior'],
        title='Customer Value Analysis: Engagement vs Lifetime Value',
        labels={
            'engagement_score': 'Engagement Score',
            'lifetime_value': 'Lifetime Value (₹)'
        },
        color_discrete_map={
            'new': '#4CAF50',
            'returning': '#2196F3',
            'vip': '#FFC107',
            'at_risk': '#F44336'
        }
    )
    
    fig.update_layout(height=600)
    
    return fig


def create_channel_performance_chart(
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a bar chart showing performance metrics by order channel.
    
    Args:
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    if 'channel' not in orders_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Channel data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    channel_metrics = orders_df.groupby('channel').agg({
        'amount': ['sum', 'mean', 'count']
    }).reset_index()
    
    channel_metrics.columns = ['channel', 'total_revenue', 'avg_order_value', 'order_count']
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Total Revenue', 'Average Order Value', 'Order Count'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
    )
    
    colors = {'web': '#0066cc', 'app': '#28a745', 'store': '#FFC107'}
    
    for channel in channel_metrics['channel'].unique():
        channel_data = channel_metrics[channel_metrics['channel'] == channel]
        color = colors.get(channel, '#999999')
        
        fig.add_trace(
            go.Bar(
                x=[channel],
                y=channel_data['total_revenue'],
                name=channel,
                marker_color=color,
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=[channel],
                y=channel_data['avg_order_value'],
                name=channel,
                marker_color=color,
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(
                x=[channel],
                y=channel_data['order_count'],
                name=channel,
                marker_color=color,
                showlegend=True
            ),
            row=1, col=3
        )
    
    fig.update_layout(
        title_text='Channel Performance Analysis',
        height=400,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="Revenue (₹)", row=1, col=1)
    fig.update_yaxes(title_text="Avg Value (₹)", row=1, col=2)
    fig.update_yaxes(title_text="Orders", row=1, col=3)
    
    return fig


def create_acquisition_funnel_chart(
    customers_df: pd.DataFrame
) -> go.Figure:
    """
    Create a detailed customer acquisition and lifecycle funnel.
    
    Args:
        customers_df: Customer dataframe
    
    Returns:
        Plotly Figure object
    """
    total = len(customers_df)
    new_customers = customers_df[customers_df['segment'] == 'new'].shape[0]
    returning = customers_df[customers_df['segment'] == 'returning'].shape[0]
    vip = customers_df[customers_df['segment'] == 'vip'].shape[0]
    
    # Calculate engagement levels
    high_engagement = customers_df[customers_df.get('engagement_score', 0) > 70].shape[0]
    
    fig = go.Figure(go.Funnel(
        y=['Total Customers', 'New Customers', 'Returning Customers', 'VIP Customers', 'High Engagement'],
        x=[total, new_customers, returning, vip, high_engagement],
        textposition="inside",
        textinfo="value+percent previous",
        marker=dict(
            color=['#0066cc', '#4CAF50', '#2196F3', '#FFC107', '#FF5722'],
            line=dict(width=2, color='white')
        ),
        connector=dict(line=dict(color='#888888', width=2))
    ))
    
    fig.update_layout(
        title='Customer Acquisition & Lifecycle Funnel',
        height=500
    )
    
    return fig


def create_product_category_trends(
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a line chart showing product category trends over time.
    
    Args:
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    if 'product_category' not in orders_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Product category data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    orders_copy = orders_df.copy()
    orders_copy['order_date'] = pd.to_datetime(orders_copy['order_date'])
    orders_copy['month'] = orders_copy['order_date'].dt.to_period('M')
    
    category_trends = orders_copy.groupby(['month', 'product_category'])['amount'].sum().reset_index()
    category_trends['month_str'] = category_trends['month'].astype(str)
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    for i, category in enumerate(category_trends['product_category'].unique()):
        cat_data = category_trends[category_trends['product_category'] == category]
        fig.add_trace(go.Scatter(
            x=cat_data['month_str'],
            y=cat_data['amount'],
            mode='lines+markers',
            name=category.title(),
            line=dict(width=2, color=colors[i % len(colors)]),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title='Product Category Revenue Trends Over Time',
        xaxis_title='Month',
        yaxis_title='Revenue (₹)',
        height=500,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


def create_response_rate_analysis(
    customers_df: pd.DataFrame
) -> go.Figure:
    """
    Create a chart analyzing customer response rates by segment and behavior.
    
    Args:
        customers_df: Customer dataframe
    
    Returns:
        Plotly Figure object
    """
    if 'response_rate' not in customers_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Response rate data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Response rate by segment
    segment_response = customers_df.groupby('segment')['response_rate'].mean().reset_index()
    segment_response['response_rate_pct'] = segment_response['response_rate'] * 100
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Response Rate by Segment', 'Response Rate Distribution'),
        specs=[[{'type': 'bar'}, {'type': 'box'}]]
    )
    
    colors = {'new': '#4CAF50', 'returning': '#2196F3', 
              'vip': '#FFC107', 'at_risk': '#F44336'}
    
    for segment in segment_response['segment']:
        seg_data = segment_response[segment_response['segment'] == segment]
        fig.add_trace(
            go.Bar(
                x=[segment],
                y=seg_data['response_rate_pct'],
                name=segment,
                marker_color=colors.get(segment, '#999999'),
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Box plot for distribution
    for segment in customers_df['segment'].unique():
        seg_customers = customers_df[customers_df['segment'] == segment]
        fig.add_trace(
            go.Box(
                y=seg_customers['response_rate'] * 100,
                name=segment,
                marker_color=colors.get(segment, '#999999')
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        title_text='Customer Response Rate Analysis',
        height=400,
        showlegend=False
    )
    
    fig.update_yaxes(title_text="Response Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Response Rate (%)", row=1, col=2)
    
    return fig


def create_buying_behavior_chart(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> go.Figure:
    """
    Create a chart showing metrics by buying behavior type.
    
    Args:
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    
    Returns:
        Plotly Figure object
    """
    if 'buying_behavior' not in customers_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Buying behavior data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    behavior_metrics = []
    
    for behavior in customers_df['buying_behavior'].unique():
        behav_customers = customers_df[customers_df['buying_behavior'] == behavior]
        behav_orders = orders_df[orders_df['customer_id'].isin(behav_customers['customer_id'])]
        
        metrics = {
            'behavior': behavior,
            'customer_count': len(behav_customers),
            'total_revenue': behav_orders['amount'].sum(),
            'avg_order_value': behav_orders['amount'].mean() if len(behav_orders) > 0 else 0
        }
        behavior_metrics.append(metrics)
    
    metrics_df = pd.DataFrame(behavior_metrics)
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Customer Count', 'Total Revenue', 'Avg Order Value'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
    )
    
    colors = px.colors.qualitative.Set3
    
    for i, behavior in enumerate(metrics_df['behavior']):
        behav_data = metrics_df[metrics_df['behavior'] == behavior]
        color = colors[i % len(colors)]
        
        fig.add_trace(
            go.Bar(
                x=[behavior],
                y=behav_data['customer_count'],
                marker_color=color,
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=[behavior],
                y=behav_data['total_revenue'],
                marker_color=color,
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(
                x=[behavior],
                y=behav_data['avg_order_value'],
                marker_color=color,
                showlegend=True,
                name=behavior
            ),
            row=1, col=3
        )
    
    fig.update_layout(
        title_text='Performance by Buying Behavior',
        height=400,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Revenue (₹)", row=1, col=2)
    fig.update_yaxes(title_text="Avg Value (₹)", row=1, col=3)
    
    return fig

