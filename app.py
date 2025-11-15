"""
AI-Powered Business Intelligence Streamlit Dashboard.
Main entry point for the application.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

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
from bi import analysis, visuals
from media import tts, ai_images, video
from notifier import email_webhook


# Page configuration
st.set_page_config(
    page_title="AI BI Reports Dashboard",
    page_icon="📊",
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
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0066cc;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
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


def add_log(message: str, level: str = "info"):
    """Add a log message to session state."""
    st.session_state.logs.append({"message": message, "level": level})
    if level == "error":
        logger.error(message)
    elif level == "success":
        logger.info(f"✓ {message}")
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
    st.markdown('<div class="main-header">📊 AI-Powered BI Reports Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Automated Business Intelligence with Data Generation, Analysis, Visualization, and Delivery**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        st.subheader("📁 Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate Data", width='stretch'):
                with st.spinner("Generating synthetic data..."):
                    try:
                        customers_df, orders_df = generator.generate_synthetic_data()
                        generator.save_data(customers_df, orders_df)
                        st.session_state.customers_df = customers_df
                        st.session_state.orders_df = orders_df
                        add_log("New data generated successfully!", "success")
                        st.rerun()
                    except Exception as e:
                        add_log(f"Error generating data: {e}", "error")
                        st.error(f"Error: {e}")
        
        with col2:
            if st.button("📥 Reload Data", width='stretch'):
                st.session_state.customers_df = None
                st.session_state.orders_df = None
                load_data_if_needed()
                st.rerun()
        
        # Load data if needed
        load_data_if_needed()
        
        st.markdown("---")
        
        # Customer selection
        if st.session_state.customers_df is not None:
            st.subheader("👤 Select Customer")
            
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
        st.subheader("🤖 AI Options")
        use_openai = st.checkbox("Use OpenAI (DALL-E)", value=False, help="Requires OPENAI_API_KEY in .env")
        use_gemini = st.checkbox("Use Gemini", value=False, help="Requires GOOGLE_API_KEY in .env")
        
        st.markdown("---")
        
        # Actions
        if st.session_state.selected_customer_id:
            st.subheader("⚡ Actions")
            
            if st.button("🔊 Generate Audio", width='stretch'):
                generate_audio_action(st.session_state.selected_customer_id)
            
            if st.button("🎬 Generate Video", width='stretch'):
                generate_video_action(st.session_state.selected_customer_id, use_openai, use_gemini)
            
            if st.button("📧 Send Email", width='stretch'):
                send_email_action(st.session_state.selected_customer_id)
    
    # Main content
    if st.session_state.customers_df is None:
        st.info("👈 Click 'Generate Data' or 'Reload Data' in the sidebar to get started.")
        return
    
    if not st.session_state.selected_customer_id:
        st.info("👈 Select a customer from the sidebar to view their profile.")
        return
    
    # Display customer profile and analytics
    display_customer_dashboard(st.session_state.selected_customer_id)
    
    # Display logs
    with st.expander("📋 Activity Log", expanded=False):
        if st.session_state.logs:
            for log_entry in reversed(st.session_state.logs[-20:]):  # Show last 20
                level = log_entry['level']
                message = log_entry['message']
                if level == "error":
                    st.markdown(f'<span class="status-error">❌ {message}</span>', unsafe_allow_html=True)
                elif level == "success":
                    st.markdown(f'<span class="status-success">✅ {message}</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="status-info">ℹ️ {message}</span>', unsafe_allow_html=True)
        else:
            st.write("No activity yet.")


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
        st.subheader(f"👤 {customer['name']}")
        st.write(f"**ID:** {customer['customer_id']}")
        st.write(f"**Email:** {customer['email']}")
    
    with col2:
        # Segment badge
        segment_colors = {
            'new': '🟢', 'returning': '🔵', 
            'vip': '🟡', 'at_risk': '🔴'
        }
        st.write(f"**Segment:** {segment_colors.get(customer['segment'], '⚪')} {customer['segment'].upper()}")
        st.write(f"**Interests:** {', '.join(customer['interests'])}")
    
    with col3:
        st.write(f"**Last Contact:** {customer['last_contact_date']}")
        st.write(f"**Member Since:** {customer['created_at']}")
    
    st.markdown("---")
    
    # KPIs
    st.subheader("📊 Key Performance Indicators")
    
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
    st.subheader("📈 Analytics")
    
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
    st.subheader("🎬 Generated Media")
    
    subdirs = config.get_customer_subdirs(customer_id)
    
    media_col1, media_col2 = st.columns(2)
    
    with media_col1:
        st.write("**🔊 Audio Summary**")
        audio_path = subdirs['audio'] / "summary.mp3"
        if audio_path.exists():
            st.audio(str(audio_path))
            st.success(f"Audio file: {audio_path.name}")
        else:
            st.info("No audio generated yet. Click 'Generate Audio' in the sidebar.")
    
    with media_col2:
        st.write("**📹 Video Report**")
        video_path = subdirs['video'] / f"report_{customer_id}.mp4"
        if video_path.exists():
            st.video(str(video_path))
            st.success(f"Video file: {video_path.name}")
            
            # Download button
            with open(video_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Download Video",
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
                st.success(f"✅ Audio generated: {audio_path.name}")
                st.rerun()
            else:
                add_log(f"Failed to generate audio for {customer['name']}", "error")
                st.error("❌ Failed to generate audio")
                
        except Exception as e:
            add_log(f"Audio generation error: {e}", "error")
            st.error(f"❌ Error: {e}")


def generate_video_action(customer_id: str, use_openai: bool, use_gemini: bool):
    """Generate video for a customer."""
    with st.spinner("Generating video (this may take a minute)..."):
        try:
            customers_df = st.session_state.customers_df
            orders_df = st.session_state.orders_df
            
            customer = analysis.get_customer_profile(customer_id, customers_df)
            kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
            
            subdirs = config.get_customer_subdirs(customer_id)
            
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
                subdirs['video'] / f"report_{customer_id}.mp4"
            )
            
            if video_path:
                add_log(f"Video generated for {customer['name']}", "success")
                st.success(f"✅ Video generated: {video_path.name}")
                st.rerun()
            else:
                add_log(f"Failed to generate video for {customer['name']}", "error")
                st.error("❌ Failed to generate video")
                
        except Exception as e:
            add_log(f"Video generation error: {e}", "error")
            st.error(f"❌ Error: {e}")
            import traceback
            st.code(traceback.format_exc())


def send_email_action(customer_id: str):
    """Send email report for a customer."""
    with st.spinner("Sending email..."):
        try:
            if not config.APPS_SCRIPT_WEBHOOK_URL:
                st.warning("⚠️ Apps Script webhook URL not configured. Set APPS_SCRIPT_WEBHOOK_URL in .env file.")
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
                st.success(f"✅ Email sent to {customer['email']}")
            else:
                add_log(f"Failed to send email to {customer['email']}", "error")
                st.error("❌ Failed to send email")
                
        except Exception as e:
            add_log(f"Email sending error: {e}", "error")
            st.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
