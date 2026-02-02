# 💔 Healing Horizons - Breakup Recovery Assistant

A modern, AI-powered web application designed to help individuals navigate breakup recovery with personalized support, tracking, and community features. Built with 2026 design standards and specifically tailored for the Indian context.

## 🌟 Features

### 🤖 AI-Powered Assistance
- **Therapist Agent**: Empathetic counseling with cultural understanding
- **Closure Specialist**: Help with unsaid feelings and emotional release
- **Recovery Planner**: Personalized 7/14/30-day recovery plans
- **Brutal Honesty**: Direct, motivational tough-love advice

### 📊 Personal Dashboard
- Mood tracking with interactive charts
- Progress monitoring across multiple dimensions
- Journal with mood analysis and writing prompts
- Achievement milestones and streaks

### 🏛️ Indian Context
- Culturally relevant advice and examples
- Local helplines and resources
- Support for Indian languages (coming soon)
- Regional therapist directories

### 👥 Community Features
- Anonymous sharing space
- Group healing activities
- Expert Q&A sessions
- Support groups by city

### 🔒 Privacy & Security
- End-to-end encryption for sensitive data
- Anonymous journal options
- GDPR/Indian Data Protection compliant
- No data sharing with third parties

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API key
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/healing-horizons.git
cd healing-horizons
```

2. **Create a virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file or `config.py`:
```python
GROQ_API_KEY = 'your_groq_api_key_here'
SECRET_KEY = 'your_secret_key_here'
```

5. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## ⚠️ Troubleshooting

### Groq API Rate Limit Error

**Problem:** You see errors like:
```
Rate limit reached for model llama-3.3-70b-versatile
Limit 100000, Used 99997, Requested 125
```

**What This Means:**
- Groq's free tier has a limit of **100,000 tokens per day**
- Each AI agent call uses tokens (roughly 100-500 tokens per request)
- With 4 agents per plan generation, you can hit this limit quickly

**Solutions:**

#### 1. **Use Built-in Fallback Responses** ✅ (Already Implemented)
The application now automatically detects rate limit errors and shows pre-generated, high-quality recovery guidance. You'll see a message:
> "⚠️ AI service is temporarily at capacity. Showing pre-generated recovery guidance."

**No action needed** - the app will continue working with fallback content!

#### 2. **Upgrade Your Groq Account** 💰
- Visit: https://console.groq.com/settings/billing
- Upgrade to **Dev Tier** for higher limits
- Cost: Varies by usage

#### 3. **Use Alternative AI Providers** 🔄
You can switch to other providers by modifying `app.py`:

**Option A: OpenAI**
```python
from agno.models.openai import OpenAI
model = OpenAI(id="gpt-4", api_key=openai_key)
```

**Option B: Anthropic Claude**
```python
from agno.models.anthropic import Claude
model = Claude(id="claude-3-sonnet", api_key=anthropic_key)
```

**Option C: Google Gemini**
```python
from agno.models.google import Gemini
model = Gemini(id="gemini-pro", api_key=google_key)
```

#### 4. **Reduce Token Usage** 📉
Edit the agent instructions in `app.py` (lines 68-119) to be more concise:
```python
instructions=[
    "Brief, focused advice only",
    "Maximum 200 words per response"
]
```

#### 5. **Wait for Reset** ⏰
The rate limit resets every 24 hours. Check the error message for exact reset time:
> "Please try again in 1m45.408s"

---

## 🎯 Features in Detail

### 🤖 AI-Powered Assistance
- **Therapist Agent**: Empathetic counseling with cultural understanding
- **Closure Specialist**: Help with unsaid feelings and emotional release
- **Recovery Planner**: Personalized 7/14/30-day recovery plans
- **Brutal Honesty**: Direct, motivational tough-love advice

### 📊 Personal Dashboard
- Mood tracking with interactive charts
- Progress monitoring across multiple dimensions
- Journal with mood analysis and writing prompts
- Achievement milestones and streaks

### 🏛️ Indian Context
- Culturally relevant advice and examples
- Local helplines and resources
- Support for Indian languages (coming soon)
- Regional therapist directories

### 👥 Community Features
- Anonymous sharing space
- Group healing activities
- Expert Q&A sessions
- Support groups by city

### 🔒 Privacy & Security
- End-to-end encryption for sensitive data
- Anonymous journal options
- GDPR/Indian Data Protection compliant
- No data sharing with third parties

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API key (or alternative AI provider)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/healing-horizons.git
cd healing-horizons