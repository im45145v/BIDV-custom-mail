"""
AI-Powered Business Intelligence Streamlit Dashboard.
Enhanced with personalized sales pitch generation and advanced analytics.
Main entry point for the application.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
import io

import streamlit as st
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import project modules
import config
from data import generator
from bi import analysis, visuals, sales_pitch
from media import tts, ai_images, video
from notifier import email_webhook


# Page configuration
st.set_page_config(
    page_title="AI Sales Pitch Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-info {
        color: #17a2b8;
        font-weight: bold;
    }
    .tab-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'customers_df' not in st.session_state:
        st.session_state.customers_df = None
    if 'orders_df' not in st.session_state:
        st.session_state.orders_df = None
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'selected_customer_id' not in st.session_state:
        st.session_state.selected_customer_id = None
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Customer View"


def add_log(message: str, level: str = "info"):
    """Add a log message to session state."""
    st.session_state.logs.append({"message": message, "level": level})
    if level == "error":
        logger.error(message)
    elif level == "success":
        logger.info(message)
    else:
        logger.info(message)


def load_data_if_needed():
    """Load data into session state if not already loaded."""
    if st.session_state.customers_df is None or st.session_state.orders_df is None:
        try:
            customers_df, orders_df = generator.ensure_data_exists()
            st.session_state.customers_df = customers_df
            st.session_state.orders_df = orders_df
            add_log(f"Data loaded: {len(customers_df)} customers, {len(orders_df)} orders", "success")
        except Exception as e:
            add_log(f"Error loading data: {e}", "error")


def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🎯 AI-Powered Sales Pitch Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Personalized Sales Intelligence with Advanced Analytics & Customer Insights**")
    st.markdown("**Note: Audio/Video Generation and Email has been disabled. If you want please contact the Repo owner and make them enable it. This has been done keeping in mind that public end points are insecure (Project by Ashish Malla)**")

    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Panel")
        
        st.subheader("🗂 Data Management")
        
        # Data generation and upload
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Data ⚡", width='stretch'):
                with st.spinner("Generating 1000 customer records..."):
                    try:
                        customers_df, orders_df = generator.generate_synthetic_data()
                        generator.save_data(customers_df, orders_df)
                        st.session_state.customers_df = customers_df
                        st.session_state.orders_df = orders_df
                        add_log(f"Generated {len(customers_df)} customers with {len(orders_df)} orders!", "success")
                        st.rerun()
                    except Exception as e:
                        add_log(f"Error generating data: {e}", "error")
                        st.error(f"Error: {e}")
        
        with col2:
            if st.button("Reload Data", width='stretch'):
                st.session_state.customers_df = None
                st.session_state.orders_df = None
                load_data_if_needed()
                st.rerun()
        
        # Upload dataset
        st.subheader("📤 Upload Custom Dataset")
        uploaded_customers = st.file_uploader("Upload Customers CSV", type=['csv'], key="cust_upload")
        uploaded_orders = st.file_uploader("Upload Orders CSV", type=['csv'], key="ord_upload")
        
        if uploaded_customers and uploaded_orders:
            if st.button("Load Uploaded Data"):
                try:
                    customers_df, orders_df = generator.load_uploaded_data(
                        uploaded_customers, uploaded_orders
                    )
                    st.session_state.customers_df = customers_df
                    st.session_state.orders_df = orders_df
                    add_log(f"Loaded {len(customers_df)} customers from upload", "success")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading files: {e}")
        
        # Download example dataset
        if st.button("Download Example Dataset"):
            try:
                ex_cust, ex_ord = generator.create_example_dataset()
                
                # Convert to CSV for download
                cust_csv = ex_cust.to_csv(index=False).encode('utf-8')
                ord_csv = ex_ord.to_csv(index=False).encode('utf-8')
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "Customers.csv",
                        cust_csv,
                        "example_customers.csv",
                        "text/csv",
                        width='stretch'
                    )
                with col_b:
                    st.download_button(
                        "Orders.csv",
                        ord_csv,
                        "example_orders.csv",
                        "text/csv",
                        width='stretch'
                    )
            except Exception as e:
                st.error(f"Error creating example: {e}")
        
        # Load data if needed
        load_data_if_needed()
        
        st.markdown("---")
        
        # Customer selection
        if st.session_state.customers_df is not None:
            st.subheader("Select Customer")
            
            customers_df = st.session_state.customers_df
            customer_options = customers_df['customer_id'].tolist()
            customer_names = customers_df['name'].tolist()
            customer_display = [f"{cid} - {name}" for cid, name in zip(customer_options, customer_names)]
            
            selected_display = st.selectbox(
                "Customer",
                customer_display,
                key="customer_selector"
            )
            
            if selected_display:
                st.session_state.selected_customer_id = selected_display.split(" - ")[0]
        
        st.markdown("---")
        
        # AI options
        st.subheader("AI Options")
        use_openai = st.checkbox("Use OpenAI (DALL-E)", value=False, help="Requires OPENAI_API_KEY in .env")
        use_gemini = st.checkbox("Use Gemini", value=False, help="Requires GOOGLE_API_KEY in .env")
        use_veo3 = st.checkbox("Use Veo3 for Video", value=False, help="Generate videos with Veo3 using sales pitch")
        
        st.markdown("---")
        
        # Actions
        if st.session_state.selected_customer_id:
            st.subheader("Actions")
            
            if st.button("Generate Sales Pitch ✉️", width='stretch'):
                generate_sales_pitch_action(st.session_state.selected_customer_id)
            
            if st.button("Generate Audio 🔊", width='stretch'):
                generate_audio_action(st.session_state.selected_customer_id)
            
            if st.button("Generate Video 🎬", width='stretch'):
                generate_video_action(st.session_state.selected_customer_id, use_openai, use_gemini, use_veo3)
            
            if st.button("Send Sales Pitch ✉️", width='stretch'):
                send_sales_pitch_action(st.session_state.selected_customer_id)

            if st.button("Send Email ✉️", width='stretch'):
                send_email_action(st.session_state.selected_customer_id)
    
    # Main content - Tabs
    if st.session_state.customers_df is None:
        st.info("Click 'Generate Data' or 'Upload Custom Dataset' in the sidebar to get started.")
        return
    
    # Create tabs
    tab1, tab2 = st.tabs(["Customer View", "📊 All Users Analytics"])
    
    with tab1:
        display_customer_view()
    
    with tab2:
        display_all_users_analytics()
    
    # Display logs at bottom
    with st.expander("Activity Log", expanded=False):
        if st.session_state.logs:
            for log_entry in reversed(st.session_state.logs[-20:]):  # Show last 20
                level = log_entry['level']
                message = log_entry['message']
                if level == "error":
                    st.markdown(f'<span class="status-error">ERROR: {message}</span>', unsafe_allow_html=True)
                elif level == "success":
                    st.markdown(f'<span class="status-success">SUCCESS: {message}</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="status-info">INFO: {message}</span>', unsafe_allow_html=True)
        else:
            st.write("No activity yet.")


def display_customer_view():
    """Display customer-specific view."""
    if not st.session_state.selected_customer_id:
        st.info("Select a customer from the sidebar to view their profile.")
        return
    
    display_customer_dashboard(st.session_state.selected_customer_id)


def display_all_users_analytics():
    """Display analytics for all users."""
    st.markdown('<div class="tab-header">📊 All Users Analytics Dashboard</div>', unsafe_allow_html=True)
    
    customers_df = st.session_state.customers_df
    orders_df = st.session_state.orders_df
    
    # Overall KPIs
    st.subheader("🎯 Overall Business Metrics")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(customers_df)}</div>
            <div class="kpi-label">Total Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        total_revenue = orders_df['amount'].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">₹{total_revenue:,.0f}</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        avg_ltv = customers_df['lifetime_value'].mean() if 'lifetime_value' in customers_df.columns else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">₹{avg_ltv:,.0f}</div>
            <div class="kpi-label">Avg Customer LTV</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        avg_engagement = customers_df['engagement_score'].mean() if 'engagement_score' in customers_df.columns else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_engagement:.0f}%</div>
            <div class="kpi-label">Avg Engagement</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Customer Journey Funnel")
        try:
            fig_funnel = visuals.create_funnel_chart(customers_df, orders_df)
            st.plotly_chart(fig_funnel, width='stretch')
        except Exception as e:
            st.error(f"Error creating funnel chart: {e}")
    
    with col2:
        st.subheader("📈 Segment Distribution")
        segment_df = analysis.get_overall_segment_distribution(customers_df)
        fig_seg = visuals.create_segment_distribution_chart(segment_df)
        st.pyplot(fig_seg)
    
    st.markdown("---")
    
    # Engagement Heatmap
    st.subheader("🔥 Engagement Heatmap: Segment vs Buying Behavior")
    try:
        fig_heatmap = visuals.create_engagement_heatmap(customers_df)
        st.plotly_chart(fig_heatmap, width='stretch')
    except Exception as e:
        st.error(f"Error creating heatmap: {e}")
    
    st.markdown("---")
    
    # Customer Value Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💎 Lifetime Value Distribution")
        try:
            fig_ltv = visuals.create_ltv_distribution(customers_df)
            st.plotly_chart(fig_ltv, width='stretch')
        except Exception as e:
            st.error(f"Error creating LTV chart: {e}")
    
    with col2:
        st.subheader("🎯 Engagement vs Value")
        try:
            fig_scatter = visuals.create_customer_value_scatter(customers_df, orders_df)
            st.plotly_chart(fig_scatter, width='stretch')
        except Exception as e:
            st.error(f"Error creating scatter plot: {e}")
    
    st.markdown("---")
    
    # Segment Comparison Radar
    st.subheader("🕸️ Segment Performance Comparison")
    try:
        fig_radar = visuals.create_segment_comparison_chart(customers_df, orders_df)
        st.plotly_chart(fig_radar, width='stretch')
    except Exception as e:
        st.error(f"Error creating radar chart: {e}")
    
    st.markdown("---")
    
    # Revenue Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue by Category")
        category_df = analysis.get_overall_category_share(orders_df)
        fig_cat = visuals.create_overall_category_chart(category_df)
        st.pyplot(fig_cat)
    
    with col2:
        st.subheader("📈 Monthly Revenue Trends")
        try:
            fig_monthly = visuals.create_monthly_trend_comparison(orders_df)
            st.plotly_chart(fig_monthly, width='stretch')
        except Exception as e:
            st.error(f"Error creating monthly trend: {e}")
    
    st.markdown("---")
    
    # Cohort Analysis
    st.subheader("👥 Customer Retention Analysis")
    try:
        fig_cohort = visuals.create_cohort_retention_chart(customers_df, orders_df)
        st.plotly_chart(fig_cohort, width='stretch')
    except Exception as e:
        st.error(f"Error creating cohort chart: {e}")
    
    st.markdown("---")
    
    # NEW CHARTS SECTION
    st.subheader("📊 Additional Analytics")
    
    # Channel Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Channel Performance**")
        try:
            fig_channel = visuals.create_channel_performance_chart(orders_df)
            st.plotly_chart(fig_channel, width='stretch')
        except Exception as e:
            st.error(f"Error creating channel chart: {e}")
    
    with col2:
        st.write("**Acquisition Funnel**")
        try:
            fig_acquisition = visuals.create_acquisition_funnel_chart(customers_df)
            st.plotly_chart(fig_acquisition, width='stretch')
        except Exception as e:
            st.error(f"Error creating acquisition funnel: {e}")
    
    st.markdown("---")
    
    # Product Category Trends
    st.subheader("📈 Product Category Trends")
    try:
        fig_cat_trends = visuals.create_product_category_trends(orders_df)
        st.plotly_chart(fig_cat_trends, width='stretch')
    except Exception as e:
        st.error(f"Error creating category trends: {e}")
    
    st.markdown("---")
    
    # Response Rate and Buying Behavior
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Response Rate Analysis**")
        try:
            fig_response = visuals.create_response_rate_analysis(customers_df)
            st.plotly_chart(fig_response, width='stretch')
        except Exception as e:
            st.error(f"Error creating response rate chart: {e}")
    
    with col2:
        st.write("**Buying Behavior Performance**")
        try:
            fig_behavior = visuals.create_buying_behavior_chart(customers_df, orders_df)
            st.plotly_chart(fig_behavior, width='stretch')
        except Exception as e:
            st.error(f"Error creating buying behavior chart: {e}")
    
    # Data table
    st.markdown("---")
    st.subheader("📋 Customer Data Table")
    
    # Display options
    col1, col2, col3 = st.columns(3)
    with col1:
        segment_filter = st.multiselect(
            "Filter by Segment",
            options=customers_df['segment'].unique().tolist(),
            default=customers_df['segment'].unique().tolist()
        )
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=['lifetime_value', 'engagement_score', 'response_rate', 'name']
        )
    with col3:
        sort_order = st.selectbox("Order", options=['Descending', 'Ascending'])
    
    # Filter and sort
    filtered_df = customers_df[customers_df['segment'].isin(segment_filter)]
    ascending = (sort_order == 'Ascending')
    filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
    
    # Display table with selected columns
    display_cols = ['customer_id', 'name', 'email', 'segment', 'lifetime_value', 
                    'engagement_score', 'buying_behavior', 'response_rate']
    st.dataframe(
        filtered_df[display_cols].head(50),
        width='stretch',
        hide_index=True
    )


def generate_sales_pitch_action(customer_id: str):
    """Generate and display sales pitch for a customer."""
    with st.spinner("Generating personalized sales pitch..."):
        try:
            customers_df = st.session_state.customers_df
            orders_df = st.session_state.orders_df
            
            customer = analysis.get_customer_profile(customer_id, customers_df)
            kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
            
            # Generate pitch
            pitch = sales_pitch.generate_sales_pitch(
                customer['name'],
                customer['segment'],
                customer.get('interests', []),
                customer.get('pain_points', []),
                customer.get('buying_behavior', 'researcher'),
                customer.get('engagement_score', 50),
                kpis
            )
            
            # Generate recommendations
            recommendations = sales_pitch.generate_recommendations(
                customer.get('interests', []),
                kpis,
                customer['segment']
            )
            
            # Display pitch
            st.success("Sales pitch generated successfully!")
            
            with st.expander("View Generated Sales Pitch", expanded=True):
                st.write("**Subject Line:**")
                st.info(pitch['subject'])
                
                st.write("**Opening:**")
                st.write(pitch['opening'])
                
                st.write("**Body:**")
                st.write(pitch['body'])
                
                st.write("**Call to Action:**")
                st.write(pitch['cta'])
                
                st.write("**Closing:**")
                st.write(pitch['closing'])
                
                st.markdown("---")
                st.write("**Recommendations:**")
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. **{rec['title']}** - {rec['description']} ({rec['discount']})")
            
            add_log(f"Sales pitch generated for {customer['name']}", "success")
            
        except Exception as e:
            add_log(f"Sales pitch generation error: {e}", "error")
            st.error(f"Error: {e}")


def display_customer_dashboard(customer_id: str):
    """Display customer profile and analytics."""
    customers_df = st.session_state.customers_df
    orders_df = st.session_state.orders_df
    
    # Get customer data
    customer = analysis.get_customer_profile(customer_id, customers_df)
    if not customer:
        st.error(f"Customer {customer_id} not found.")
        return
    
    kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
    
    # Customer profile card
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.subheader(f"{customer['name']}")
        st.write(f"**ID:** {customer['customer_id']}")
        st.write(f"**Email:** {customer['email']}")
    
    with col2:
        # Segment label
        st.write(f"**Segment:** {customer['segment'].capitalize()}")
        st.write(f"**Interests:** {', '.join(customer['interests'])}")
    
    with col3:
        st.write(f"**Last Contact:** {customer['last_contact_date']}")
        st.write(f"**Member Since:** {customer['created_at']}")
    
    st.markdown("---")
    
    # KPIs
    st.subheader("Key Performance Indicators")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">₹{kpis['total_spend']:,.0f}</div>
            <div class="kpi-label">Total Spend</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['orders_count']}</div>
            <div class="kpi-label">Orders Placed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">₹{kpis['average_order_value']:,.0f}</div>
            <div class="kpi-label">Average Order Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['order_frequency']:.1f}</div>
            <div class="kpi-label">Orders/Month</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    st.subheader("Analytics")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("**Spending Trend (Last 90 Days)**")
        trend_df = analysis.get_recent_trend(customer_id, orders_df, days=90)
        if len(trend_df) > 0:
            fig = visuals.create_plotly_spend_chart(trend_df, customer['name'])
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No recent orders to display.")
    
    with chart_col2:
        st.write("**Category Spending**")
        category_df = analysis.get_category_distribution(customer_id, orders_df)
        if len(category_df) > 0:
            import plotly.express as px
            fig = px.bar(category_df, x='amount', y='category', orientation='h',
                        labels={'amount': 'Spend (₹)', 'category': 'Category'})
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No orders to display.")
    
    st.markdown("---")
    
    # Media section
    st.subheader("Generated Media")
    
    subdirs = config.get_customer_subdirs(customer_id)
    
    media_col1, media_col2 = st.columns(2)
    
    with media_col1:
        st.write("**Audio Summary**")
        audio_path = subdirs['audio'] / "summary.mp3"
        if audio_path.exists():
            st.audio(str(audio_path))
            st.success(f"Audio file: {audio_path.name}")
        else:
            st.info("No audio generated yet. Click 'Generate Audio' in the sidebar.")
    
    with media_col2:
        st.write("**Video Report**")
        video_path = subdirs['video'] / f"report_{customer_id}.mp4"
        if video_path.exists():
            st.video(str(video_path))
            
            # Check if video was generated with Veo3
            veo3_marker = subdirs['video'] / f".veo3_generated_{customer_id}"
            if veo3_marker.exists():
                st.success(f"✨ Video generated with Veo3 AI")
            else:
                st.success(f"Video file: {video_path.name}")
            
            # Download button
            with open(video_path, 'rb') as f:
                st.download_button(
                    label="Download Video",
                    data=f,
                    file_name=f"report_{customer_id}.mp4",
                    mime="video/mp4"
                )
        else:
            st.info("No video generated yet. Click 'Generate Video' in the sidebar.")


def generate_audio_action(customer_id: str):
    """Generate audio for a customer."""
    with st.spinner("Generating audio..."):
        try:
            customers_df = st.session_state.customers_df
            orders_df = st.session_state.orders_df
            
            customer = analysis.get_customer_profile(customer_id, customers_df)
            kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
            
            summary_text = analysis.generate_summary_text(customer['name'], kpis)
            
            subdirs = config.get_customer_subdirs(customer_id)
            audio_path = tts.generate_customer_audio(
                customer['name'],
                summary_text,
                subdirs['audio']
            )
            
            if audio_path:
                add_log(f"Audio generated for {customer['name']}", "success")
                st.success(f"Audio generated: {audio_path.name}")
                st.rerun()
            else:
                add_log(f"Failed to generate audio for {customer['name']}", "error")
                st.error("Failed to generate audio")
                
        except Exception as e:
            add_log(f"Audio generation error: {e}", "error")
            st.error(f"❌ Error: {e}")


def generate_video_action(customer_id: str, use_openai: bool, use_gemini: bool, use_veo3: bool):
    """Generate video for a customer."""
    with st.spinner("Generating video (this may take a minute)..."):
        try:
            customers_df = st.session_state.customers_df
            orders_df = st.session_state.orders_df
            
            customer = analysis.get_customer_profile(customer_id, customers_df)
            kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
            
            subdirs = config.get_customer_subdirs(customer_id)
            
            # Generate sales pitch for Veo3
            sales_pitch_text = None
            if use_veo3:
                add_log("Generating sales pitch for Veo3 video...", "info")
                pitch = sales_pitch.generate_sales_pitch(
                    customer['name'],
                    customer['segment'],
                    customer.get('interests', []),
                    customer.get('pain_points', []),
                    customer.get('buying_behavior', 'researcher'),
                    customer.get('engagement_score', 50),
                    kpis
                )
                sales_pitch_text = pitch.get('full_pitch', pitch.get('body', ''))
            
            # Generate charts
            add_log("Generating charts...", "info")
            trend_df = analysis.get_recent_trend(customer_id, orders_df, days=90)
            category_df = analysis.get_category_distribution(customer_id, orders_df)
            
            charts = visuals.save_all_customer_charts(
                customer_id,
                customer['name'],
                trend_df,
                category_df,
                subdirs['charts']
            )
            
            # Generate cover image
            add_log("Generating cover image...", "info")
            cover_path = ai_images.generate_customer_image(
                customer['segment'],
                customer['interests'],
                subdirs['images'] / "ai_cover.png",
                use_openai=use_openai,
                use_gemini=use_gemini
            )
            
            # Check for audio
            audio_path = subdirs['audio'] / "summary.mp3"
            if not audio_path.exists():
                add_log("No audio found, generating...", "info")
                summary_text = analysis.generate_summary_text(customer['name'], kpis)
                audio_path = tts.generate_customer_audio(
                    customer['name'],
                    summary_text,
                    subdirs['audio']
                )
            
            # Assemble video
            add_log("Assembling video...", "info")
            video_path = video.assemble_customer_video(
                customer['name'],
                customer['segment'],
                kpis,
                charts,
                cover_path,
                audio_path,
                subdirs['video'] / f"report_{customer_id}.mp4",
                use_veo3=use_veo3,
                sales_pitch=sales_pitch_text
            )
            
            if video_path:
                add_log(f"Video generated for {customer['name']}", "success")
                st.success(f"Video generated: {video_path.name}")
                st.rerun()
            else:
                add_log(f"Failed to generate video for {customer['name']}", "error")
                st.error("Failed to generate video")
                
        except Exception as e:
            add_log(f"Video generation error: {e}", "error")
            st.error(f"Error: {e}")
            import traceback
            st.code(traceback.format_exc())


def send_email_action(customer_id: str):
    """Send email report for a customer."""
    with st.spinner("Sending email..."):
        try:
            if not config.APPS_SCRIPT_WEBHOOK_URL:
                st.warning("Apps Script webhook URL not configured. Set APPS_SCRIPT_WEBHOOK_URL in .env file.")
                add_log("Email sending skipped: webhook URL not configured", "error")
                return
            
            customers_df = st.session_state.customers_df
            orders_df = st.session_state.orders_df
            
            customer = analysis.get_customer_profile(customer_id, customers_df)
            kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
            
            success = email_webhook.send_customer_report(
                customer['name'],
                customer['email'],
                customer['segment'],
                kpis,
                video_url=None,  # Add actual URLs if hosting files
                charts_urls=None
            )
            
            if success:
                add_log(f"Email sent to {customer['email']}", "success")
                st.success(f"Email sent to {customer['email']}")
            else:
                add_log(f"Failed to send email to {customer['email']}", "error")
                st.error("Failed to send email")
                
        except Exception as e:
            add_log(f"Email sending error: {e}", "error")
            st.error(f"Error: {e}")


def send_sales_pitch_action(customer_id: str):
    """Generate a sales pitch and send it as an email via the Apps Script webhook."""
    with st.spinner("Generating and sending sales pitch..."):
        try:
            if not config.APPS_SCRIPT_WEBHOOK_URL:
                st.warning("Apps Script webhook URL not configured. Set APPS_SCRIPT_WEBHOOK_URL in .env file.")
                add_log("Sales pitch sending skipped: webhook URL not configured", "error")
                return

            customers_df = st.session_state.customers_df
            orders_df = st.session_state.orders_df

            customer = analysis.get_customer_profile(customer_id, customers_df)
            kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)

            success = sales_pitch.generate_and_send_pitch(
                customer_name=customer['name'],
                customer_email=customer['email'],
                segment=customer['segment'],
                interests=customer.get('interests', []),
                pain_points=customer.get('pain_points', []),
                buying_behavior=customer.get('buying_behavior', 'researcher'),
                engagement_score=customer.get('engagement_score', 50),
                kpis=kpis,
                attachment_urls=None
            )

            if success:
                add_log(f"Sales pitch sent to {customer['email']}", "success")
                st.success(f"Sales pitch sent to {customer['email']}")
            else:
                add_log(f"Failed to send sales pitch to {customer['email']}", "error")
                st.error("Failed to send sales pitch")

        except Exception as e:
            add_log(f"Sales pitch sending error: {e}", "error")
            st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
