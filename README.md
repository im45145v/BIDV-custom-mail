# 📊 AI-Powered Personalized Sales Pitch System

A production-ready Python + Streamlit application that implements a complete AI-powered sales intelligence pipeline with 1000-customer dataset generation, personalized sales pitch generation, advanced analytics, multi-chart visualizations, Gemini Veo video integration, and automated email delivery.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 What This Does

This project automates the entire personalized sales pitch workflow:

1. **📈 Generates 1000 synthetic customer records** with realistic behavior patterns and personalization data
2. **🎯 Creates personalized sales pitches** based on customer segments, pain points, and buying behaviors
3. **🔍 Analyzes comprehensive KPIs** including engagement scores, lifetime value, and response rates
4. **📊 Visualizes with 10+ chart types** including heatmaps, funnels, cohort analysis, and radar charts
5. **🔊 Generates audio summaries** using TTS (pyttsx3/gTTS) for each customer
6. **🎨 Creates AI-generated images** (optional: OpenAI DALL-E or Google Gemini) or placeholder images
7. **🎬 Assembles video reports** with Gemini Veo (when available) or MoviePy fallback
8. **📧 Sends personalized emails** via fun Google Apps Script webhook with happiness tracking
9. **📤 Supports dataset upload** for custom customer data analysis
10. **📊 Provides "All Users Analytics"** dashboard with business-wide insights

All controlled through a beautiful, two-tab **Streamlit dashboard**!

## 🎓 Student-Friendly

- **No paid APIs required** for core functionality
- Uses free/local tools by default (pyttsx3, PIL, matplotlib)
- Optional paid features (OpenAI, Gemini) with clear fallbacks
- Works on Mac, Linux, and Windows
- Clear documentation and examples

## 🏗️ Project Structure

```
ai_bi_streamlit_reports/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── Makefile                       # Build automation
├── run.sh                         # Quick start script
├── app.py                         # Streamlit dashboard (main entry point)
├── config.py                      # Configuration and settings
│
├── data/                          # Data generation module
│   ├── generator.py              # Synthetic data creation
│   ├── schema.py                 # Pydantic models (Customer, Order)
│   ├── customers.csv             # Generated customer data (created on first run)
│   └── orders.csv                # Generated order data (created on first run)
│
├── bi/                           # Business Intelligence module
│   ├── analysis.py               # KPI calculations and metrics
│   └── visuals.py                # Chart and graph generation
│
├── media/                        # Media generation module
│   ├── tts.py                    # Text-to-speech (pyttsx3/gTTS)
│   ├── ai_images.py              # AI image generation (OpenAI/Gemini/PIL)
│   ├── video.py                  # Video assembly (MoviePy)
│   └── output/                   # Generated media files (per customer)
│
├── notifier/                     # Email delivery module
│   ├── email_webhook.py          # Python webhook client
│   └── apps_script_sample.gs     # Google Apps Script for Gmail
│
└── tests/                        # Test suite
    ├── test_data.py              # Data generation tests
    ├── test_bi.py                # BI analysis tests
    └── test_media.py             # Media generation tests
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- FFmpeg (for video processing)

#### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/BIDV-custom-mail.git
cd BIDV-custom-mail
```

2. **Set up using Makefile (Recommended):**
```bash
make setup
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env to add API keys if you want AI features
```

### Running the App

**Option 1: Using Makefile**
```bash
make run
```

**Option 2: Using run.sh (Mac/Linux)**
```bash
./run.sh
```

**Option 3: Manual**
```bash
source venv/bin/activate
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📱 Using the Dashboard

### 1. Generate or Upload Data
- Click **"Generate Data"** in sidebar to create 1000 customers with 4000+ orders
- Or **"Upload Custom Dataset"** with your own CSV files
- Download **"Example Dataset"** (50 customers) as a template

### 2. Select a Customer
- Use the dropdown to select any customer
- View their full profile with engagement metrics

### 3. View Customer Analytics (Tab 1)
- See personalized KPIs: Total Spend, Orders, AOV, Engagement Score
- Interactive charts: Spending trend and category distribution
- View customer segment, interests, pain points, and buying behavior

### 4. Generate Sales Pitch
- Click **"Generate Sales Pitch"** to create personalized pitch
- View subject line, opening, body, CTA, and recommendations
- Pitch addresses customer's specific pain points and interests

### 5. View All Users Analytics (Tab 2)
- Overall business metrics dashboard
- Customer journey funnel visualization
- Engagement heatmaps by segment and behavior
- Lifetime value distribution analysis
- Segment performance radar charts
- Revenue trends and cohort retention
- Interactive data table with filters

### 6. Generate Media
- **Generate Audio**: Creates TTS narration of the customer summary
- **Generate Video**: Assembles a video with charts and narration (Gemini Veo or MoviePy)
- **Send Email**: Delivers personalized sales pitch via Apps Script webhook

### 7. Download/Preview
- Audio player for generated summaries
- Video player for generated reports
- Download button for video files

## 🎨 Optional AI Features

### OpenAI (DALL-E)

1. Get API key from [platform.openai.com](https://platform.openai.com/)
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```
3. Check "Use OpenAI" in the dashboard

### Google Gemini

1. Get API key from [Google AI Studio](https://makersuite.google.com/)
2. Add to `.env`:
```env
GOOGLE_API_KEY=your-key-here
```
3. Check "Use Gemini" in the dashboard

**Note:** Without API keys, the system uses PIL-generated placeholder images (still looks great!).

## 📧 Email Delivery Setup

### Deploy Google Apps Script

1. Open [Google Apps Script](https://script.google.com)
2. Create new project
3. Copy contents of `notifier/apps_script_sample.gs`
4. Deploy as Web App:
   - Click **Deploy** → **New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone** (or "Anyone with Google account")
   - Click **Deploy**
5. Copy the Web App URL
6. Add to `.env`:
```env
APPS_SCRIPT_WEBHOOK_URL=https://script.google.com/macros/s/.../exec
```

### First Run
- Apps Script will request Gmail permissions
- Approve to enable email sending

## 🧪 Running Tests

```bash
make test
```

Or manually:
```bash
source venv/bin/activate
pytest -v tests/
```

Tests cover:
- Data generation (shapes, formats, validation)
- BI analysis (KPI calculations, metrics)
- Media generation (audio, images, video handling)

## 🛠️ Troubleshooting

### TTS Issues on Linux

If `pyttsx3` fails:
```bash
sudo apt-get install espeak espeak-data libespeak-dev
```

Or use gTTS (internet required):
```python
# Automatically falls back to gTTS if pyttsx3 fails
```

### MoviePy/FFmpeg Issues

Ensure FFmpeg is installed and in PATH:
```bash
ffmpeg -version
```

If issues persist:
```bash
pip install --upgrade moviepy
```

### API Key Issues

- OpenAI: Verify key at [platform.openai.com](https://platform.openai.com/api-keys)
- Gemini: Check [Google AI Studio](https://makersuite.google.com/)
- Apps Script: Ensure deployment is "Anyone" access

### Module Not Found

Ensure virtual environment is activated:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

## 📊 Data Model

### Customer
```python
{
    "customer_id": "CUST0001",
    "name": "John Doe",
    "email": "john@example.com",
    "segment": "vip",  # new, returning, vip, at_risk
    "interests": ["fitness", "electronics"],
    "last_contact_date": "2024-01-15",
    "created_at": "2023-06-01"
}
```

### Order
```python
{
    "order_id": "ORD00000001",
    "customer_id": "CUST0001",
    "order_date": "2024-01-10",
    "amount": 2499.99,
    "product_category": "electronics",
    "channel": "web"  # web, app, store
}
```

## 🎯 Key Features

### Data Generation
- ✅ Deterministic (seed=42) for reproducibility
- ✅ Realistic names, emails (Faker)
- ✅ Segment-based spending patterns
- ✅ Interest-driven product categories

### BI Analysis
- ✅ Customer-level KPIs
- ✅ Segment distribution
- ✅ Category revenue analysis
- ✅ Time-series trends

### Visualizations
- ✅ Matplotlib for static charts
- ✅ Plotly for interactive charts
- ✅ Professional color schemes
- ✅ Currency formatting

### Media Generation
- ✅ Offline TTS (pyttsx3)
- ✅ Online TTS fallback (gTTS)
- ✅ AI image generation (optional)
- ✅ PIL placeholder images
- ✅ MoviePy video assembly

### Email Delivery
- ✅ HTML email templates
- ✅ Google Apps Script webhook
- ✅ KPI summary tables
- ✅ Media attachment links

## 🧹 Cleanup

Remove generated files:
```bash
make clean
```

This removes:
- `__pycache__` directories
- `media/output/*` files
- `.pytest_cache`

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 💡 Use Cases

- **Student Projects**: Learn data science, ML, and web development
- **Portfolio Demos**: Showcase full-stack BI capabilities
- **Prototyping**: Test BI concepts before production
- **Education**: Teach data analysis and visualization
- **Small Business**: Automate customer reporting

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [MoviePy Guide](https://zulko.github.io/moviepy/)
- [Pydantic Tutorial](https://docs.pydantic.dev/)

## ⚡ Performance Tips

- First video generation may be slow (MoviePy initialization)
- Use "Generate Data" once, then "Reload Data" for speed
- Video generation takes ~30-60 seconds per customer
- Audio generation is fast (<5 seconds)

## 🔒 Security Notes

- Never commit `.env` file (use `.env.example` template)
- Keep API keys private
- Apps Script "Anyone" access is safe (only accepts POST data)
- Validate email recipients before sending

## 📸 Screenshots

_(Add screenshots of your Streamlit dashboard here)_

### Dashboard Overview
![Dashboard](docs/screenshot_dashboard.png)

### Customer Analytics
![Analytics](docs/screenshot_analytics.png)

### Generated Video
![Video](docs/screenshot_video.png)

---

**Built with ❤️ for students and developers**

For issues or questions, please open a GitHub issue.
