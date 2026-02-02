# 💔 Healing Horizons - AI-Powered Breakup Recovery Assistant

A modern, AI-powered web application designed to help individuals navigate breakup recovery with personalized support, tracking, and community features. Built with 2026 design standards and specifically tailored for the Indian context.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI-7B68EE?style=for-the-badge)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

## 🌟 Features

### 🤖 AI-Powered Assistance
- **Therapist Agent**: Empathetic counseling with cultural understanding
- **Closure Specialist**: Help with unsaid feelings and emotional release
- **Recovery Planner**: Personalized 7/14/30-day recovery plans
- **Brutal Honesty**: Direct, motivational tough-love advice

### 📊 Personal Dashboard
- Mood tracking with interactive charts
- Progress monitoring across multiple dimensions
- Digital journal with mood analysis
- Achievement milestones and streaks

### 🏛️ Indian Context
- Culturally relevant advice and examples
- Local helplines and resources directory
- Support for Indian cultural nuances
- Regional therapist recommendations

### 👥 Community Features
- Anonymous sharing space
- Group healing activities
- Expert Q&A sessions
- City-based support groups

## 📸 Screenshots
<img width="1577" height="925" alt="Screenshot 2026-02-02 003001" src="https://github.com/user-attachments/assets/948c8724-ce35-4ff0-819b-7095aeb962f2" />

<img width="1600" height="844" alt="Screenshot 2026-02-02 003014" src="https://github.com/user-attachments/assets/f8f69c87-f7e5-4f24-85fc-522294b72bcf" />

<img width="843" height="700" alt="Screenshot 2026-02-02 003038" src="https://github.com/user-attachments/assets/52c2eaaa-32fa-4585-a1f9-33bbfb428ff8" />

<img width="871" height="826" alt="Screenshot 2026-02-02 003049" src="https://github.com/user-attachments/assets/83f83a88-461a-40d7-8cc2-c9ac8bf37a5b" />

<img width="877" height="713" alt="Screenshot 2026-02-02 003101" src="https://github.com/user-attachments/assets/e8bec4ce-4a7c-49c0-8c06-87e3a499983e" />

<img width="882" height="738" alt="Screenshot 2026-02-02 003115" src="https://github.com/user-attachments/assets/074f0898-c7ce-4ebd-bdbb-ae1bc5b8c50d" />

<img width="868" height="878" alt="Screenshot 2026-02-02 003129" src="https://github.com/user-attachments/assets/dc51f761-f349-49c6-8152-5a2fac78f49c" />

<img width="916" height="883" alt="Screenshot 2026-02-02 003141" src="https://github.com/user-attachments/assets/a5bf296c-b1be-4c67-8cfb-5c6962ab81b5" />

<img width="858" height="882" alt="Screenshot 2026-02-02 003152" src="https://github.com/user-attachments/assets/8e2f6be4-c5cd-458f-abf4-52732c4a74e1" />

<img width="847" height="882" alt="Screenshot 2026-02-02 003204" src="https://github.com/user-attachments/assets/933fbe94-aed5-4c58-bc41-ab55aad7dd28" />

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API key
- Git

### Installation

1. **Clone the repository**
```
git clone https://github.com/Pragyan2004/Healing_Horizons.git
cd Healing_Horizons
Create virtual environment
```

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
```

```
pip install -r requirements.txt

```
Configure environment
```
.env
# Edit .env with your Groq API key and other settings
```
Run
```
python app.py
Visit http://localhost:5000 to start your healing journey!
```
---
```
## 🏗️ Project Structure
text
Healing_Horizons/
├── app.py              # Main Flask application
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
├── test.py           # CLI version for testing
├── Procfile          # Deployment configuration
├── .env.example      # Environment variables template
│
├── static/           # Static assets
│   ├── css/         # Stylesheets
│   │   ├── style.css
│   │   └── animations.css
│   ├── js/          # JavaScript files
│   │   ├── main.js
│   │   └── charts.js
│   └── images/      # Images and icons
│
├── templates/        # HTML templates
│   ├── base.html    # Base template
│   ├── index.html   # Home page
│   ├── dashboard.html
│   ├── journal.html
│   ├── resources.html
│   ├── community.html
│   ├── profile.html
│   ├── results.html
│   ├── about.html
│   ├── contact.html
│   ├── privacy.html
│   └── terms.html
│
├── uploads/          # User uploads
├── instance/         # Database and instance files
└── README.md
```

---

## 🔧 Configuration
Environment Variables
Create a .env file with:
```
env
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key-here
DATABASE_URL=sqlite:///recovery.db
ENABLE_JOURNAL=true
ENABLE_COMMUNITY=true
COUNTRY=India
TIMEZONE=Asia/Kolkata
AI Model Configuration
The app uses Groq's llama-3.3-70b-versatile model by default. Modify in app.py:
python
model = Groq(id="llama-3.3-70b-versatile", api_key=api_key)
```

---

## 📱 Features in Detail

### 1. AI Therapy Sessions
Real-time emotional support

Culturally aware responses

Evidence-based techniques

Progress tracking

### 2. Digital Journal
Mood tracking with emoji selection

Writing prompts and suggestions

Tag-based organization

Export functionality

### 3. Recovery Plans
Personalized daily activities

Indian cultural context

Progress milestones

Celebratory moments

### 4. Community Support
Anonymous posting

City-based groups

Expert sessions

Resource sharing

### 5. Resource Directory
Indian helplines

Local therapists

Support groups

Self-help materials

---

## 🔐 Security Features
Password hashing with bcrypt

CSRF protection

XSS prevention

SQL injection protection

File upload validation

Session management

HTTPS enforcement (production)
---

## 📈 Performance
Lazy loading for images

Minified assets

Database indexing

Caching strategies

CDN for static assets
---

## 🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

Development Guidelines
Follow PEP 8 for Python code

Use meaningful commit messages

Write tests for new features

Update documentation
---

## 📄 License
MIT License - see LICENSE file for details
