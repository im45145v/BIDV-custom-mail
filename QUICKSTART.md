# 🚀 Quick Start Guide

## Get the App Running in 3 Steps

### Step 1: Setup (One-time)
```bash
# Install dependencies
make setup

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
# Use the quick-start script
./run.sh

# Or use Makefile
make run

# Or manually
source venv/bin/activate
streamlit run app.py
```

### Step 3: Use the Dashboard

The app will open in your browser at `http://localhost:8501`

1. **Click "Generate Data"** in the sidebar (first time only)
2. **Select a customer** from the dropdown
3. **Explore the dashboard**:
   - View KPIs (Total Spend, Orders, AOV)
   - See interactive charts
   - Generate audio summaries
   - Create video reports
   - Send email reports (optional)

---

## 📸 What You'll See

### Sidebar Controls
- 🔄 Generate Data / Reload Data buttons
- 👤 Customer selector dropdown
- 🤖 AI options (OpenAI, Gemini)
- ⚡ Action buttons (Audio, Video, Email)

### Main Dashboard
- 👤 Customer profile card
- 📊 KPI grid (4 metrics)
- 📈 Spending trend chart (interactive)
- 📊 Category spending chart
- 🔊 Audio player (if generated)
- 🎬 Video player (if generated)
- 📋 Activity log

---

## 🎯 What You Can Do

### Core Features (No API Keys Required)
✅ Generate synthetic customer and order data
✅ View detailed customer profiles and segments
✅ Analyze KPIs and spending patterns
✅ Create professional charts and visualizations
✅ Generate placeholder images for reports
✅ Test the email template formatting

### Optional Features (API Keys Required)
🔑 Generate AI images with OpenAI DALL-E
🔑 Generate AI images with Google Gemini
🔑 Send actual emails via Google Apps Script

### Media Features (System Dependent)
🔊 Generate audio narrations (requires TTS engine)
🎬 Create video reports (requires FFmpeg)

---

## 🛠️ Troubleshooting

### TTS Not Working?
```bash
# Linux
sudo apt-get install espeak espeak-data libespeak-dev

# Mac (usually works out of box)
# Windows (usually works out of box)
```

### Video Not Working?
```bash
# Install FFmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
# Windows: Download from ffmpeg.org
```

### Missing Dependencies?
```bash
pip install -r requirements.txt
```

---

## 📝 Example Workflow

### Scenario: View Customer Report

1. **Start the app**: `streamlit run app.py`
2. **Generate data**: Click "Generate Data" (creates 25 customers)
3. **Select customer**: Choose "CUST0001 - Allison Hill"
4. **View profile**: See segment (new), interests (wellness, electronics)
5. **Check KPIs**: 
   - Total Spend: ₹8,797.81
   - Orders: 5
   - AOV: ₹1,759.56
6. **See charts**: Spending trend over time, category breakdown
7. **Generate audio**: Click "Generate Audio" (creates MP3 narration)
8. **Create video**: Click "Generate Video" (assembles 30s report)
9. **Preview**: Play audio and video in dashboard
10. **Download**: Use download button for video file

---

## 🔧 Configuration (Optional)

### Add API Keys
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
APPS_SCRIPT_WEBHOOK_URL=https://script.google.com/...
```

### Google Apps Script Setup
1. Open https://script.google.com
2. Create new project
3. Copy contents from `notifier/apps_script_sample.gs`
4. Deploy as Web App
5. Copy URL to `.env` file

---

## 📚 Learn More

- **README.md** - Full documentation
- **PROJECT_SUMMARY.md** - Implementation details
- **verify.py** - Test all features
- **tests/** - Unit test examples

---

## 🎉 You're All Set!

Run `streamlit run app.py` and explore the dashboard!

Need help? Check the Activity Log panel for real-time status messages.
