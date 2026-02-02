import os
import json
from datetime import datetime, timedelta
from uuid import uuid4
from pathlib import Path
from flask import Flask, render_template, request, flash, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from agno.agent import Agent
from agno.models.groq import Groq
from agno.media import Image as AgnoImage
import markdown2
from config import Config
import signal
from functools import wraps

# Global flag to track if we're currently rate-limited
RATE_LIMITED = False
RATE_LIMIT_RESET_TIME = None

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Database setup
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------------------
# Database Models
# ------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(100), default='India')
    recovery_stage = db.Column(db.String(50), default='initial')
    
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True)
    progress = db.relationship('Progress', backref='user', lazy=True)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    mood_score = db.Column(db.Integer)  # 1-10
    activity_score = db.Column(db.Integer)  # 1-10
    social_score = db.Column(db.Integer)  # 1-10
    notes = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------------
# Helper Functions
# ------------------------------
def create_agents(api_key: str):
    """Create AI agents with enhanced instructions"""
    model = Groq(id="llama-3.1-8b-instant", api_key=api_key)
    
    therapist = Agent(
        model=model,
        name="Empathetic Therapist",
        instructions=[
            "You are Dr. Ananya Sharma, a licensed therapist specializing in relationship recovery.",
            "Use a warm, supportive tone with Indian cultural context.",
            "Provide evidence-based strategies from positive psychology and mindfulness.",
            "Structure response with: Brief Validation → Coping Strategies → Actionable Steps",
            "Include culturally relevant examples and metaphors.",
            "Format with clear headings, bullet points, and emojis for readability."
        ],
        markdown=True,
    )
    
    closure = Agent(
        model=model,
        name="Closure Specialist",
        instructions=[
            "You help write therapeutic closure messages for Indian context.",
            "Focus on: Unsent letters, forgiveness exercises, ritual suggestions.",
            "Include elements of mindfulness and letting go practices.",
            "Suggest cultural rituals like 'writing and burning' or 'river release'.",
            "Provide step-by-step emotional release exercises."
        ],
        markdown=True,
    )
    
    planner = Agent(
        model=model,
        name="Recovery Planner",
        instructions=[
            "Create personalized 14-day recovery plans for Indian users.",
            "Include daily activities: Yoga/meditation, social connections, self-care.",
            "Suggest local resources: Support groups, helplines, therapists in India.",
            "Incorporate Indian cultural activities and festivals.",
            "Add progress tracking and celebration milestones."
        ],
        markdown=True,
    )
    
    honesty = Agent(
        model=model,
        name="Brutal Honesty Coach",
        instructions=[
            "Give direct, no-filter advice with tough love approach.",
            "Use Indian idioms and colloquial language appropriately.",
            "Focus on reality checks and practical solutions.",
            "Balance harsh truths with motivational push.",
            "Include 'wake-up call' moments and empowerment messages."
        ],
        markdown=True,
    )
    
    return therapist, closure, planner, honesty

def analyze_mood(text):
    """Enhanced mood analysis from text"""
    text_lower = text.lower()
    
    # Expanded keyword lists
    positive_words = {
        'happy', 'better', 'improving', 'hope', 'healing', 'strong', 
        'good', 'great', 'awesome', 'excited', 'peace', 'calm',
        'grateful', 'love', 'joy', 'confident', 'optimistic',
        'proud', 'won', 'success', 'growth', 'smile', 'laugh'
    }
    negative_words = {
        'sad', 'pain', 'hurt', 'lonely', 'depressed', 'angry', 
        'bad', 'worse', 'broken', 'confused', 'lost', 'tears',
        'anxious', 'afraid', 'scared', 'hate', 'miss', 'crying',
        'stuck', 'guilty', 'ashamed', 'regret', 'dark', 'tired'
    }
    
    # Simple token-based scoring
    # Remove punctuation for better matching
    import string
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text_lower.translate(translator)
    
    # Crisis detection (Priority)
    crisis_keywords = {
        'die', 'suicide', 'kill', 'end it', 'no point', 'give up', 
        'death', 'hurt myself', 'tired of life', 'quit life', 'dead'
    }
    if any(keyword in clean_text for keyword in crisis_keywords):
        return "crisis"
        
    words = clean_text.split()
    
    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words)
    
    if pos_count > neg_count:
        return "improving"
    elif neg_count > pos_count:
        return "struggling"
    else:
        return "neutral"

# ------------------------------
# Routes
# ------------------------------
# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def index():
    """Home page with modern 2026 design"""
    # Auto-login a guest user for demo purposes if not logged in
    if not current_user.is_authenticated:
        guest_user = User.query.filter_by(email='guest@healing.com').first()
        if not guest_user:
            guest_user = User(
                username='Guest',
                email='guest@healing.com',
                password_hash=generate_password_hash('guest'),
                location='India',
                recovery_stage='healing'
            )
            db.session.add(guest_user)
            db.session.commit()
        login_user(guest_user)
    
    # Generate dynamic stats for homepage
    import random
    from datetime import datetime
    
    total_users = User.query.count()
    total_entries = JournalEntry.query.count()
    
    homepage_stats = {
        'healed_hearts': max(total_users * 10, random.randint(5000, 6000)),
        'journal_entries': max(total_entries, random.randint(15000, 20000)),
        'satisfaction_rate': 98,
        'local_resources': 50,
        'active_today': random.randint(200, 400)
    }
        
    return render_template('index.html', stats=homepage_stats)

# Login/Register routes removed as per request to simplify access

@app.route('/dashboard')
# @login_required - removed for easier access
def dashboard():
    """User dashboard with progress tracking"""
    # Ensure user is logged in (auto-login logic in index handles entry, but safety here)
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
        
    recent_entries = JournalEntry.query.filter_by(user_id=current_user.id)\
        .order_by(JournalEntry.created_at.desc()).limit(5).all()
    
    progress_data = Progress.query.filter_by(user_id=current_user.id)\
        .order_by(Progress.date.desc()).limit(7).all()
    
    # Calculate dynamic stats
    from datetime import datetime, timedelta
    from collections import Counter
    
    all_entries = JournalEntry.query.filter_by(user_id=current_user.id).all()
    total_entries = len(all_entries)
    
    # Calculate streak
    streak = 0
    if all_entries:
        sorted_entries = sorted(all_entries, key=lambda x: x.created_at, reverse=True)
        current_date = datetime.now().date()
        for entry in sorted_entries:
            entry_date = entry.created_at.date()
            if entry_date == current_date or entry_date == current_date - timedelta(days=streak):
                if entry_date == current_date - timedelta(days=streak):
                    streak += 1
                    current_date = entry_date
            else:
                break
    
    # Most common mood
    moods = [entry.mood for entry in all_entries if entry.mood]
    most_common_mood = Counter(moods).most_common(1)[0][0] if moods else 'neutral'
    
    # Days since start
    days_active = 0
    if all_entries:
        first_entry = min(all_entries, key=lambda x: x.created_at)
        days_active = (datetime.now() - first_entry.created_at).days + 1
    
    affirmations = [
        "I am worthy of love and respect, especially from myself.",
        "Healing is a journey, and I am taking it one day at a time.",
        "My past does not define my future; I am growing every day.",
        "I choose to let go of what I cannot control.",
        "I am resilient, strong, and capable of overcoming this.",
        "Self-love is the greatest middle finger of all time.",
        "It's okay to not be okay, as long as I keep moving forward.",
        "I deserve a life of peace and happiness.",
        "My feelings are valid, but they do not control me.",
        "Every end is a new beginning in disguise."
    ]
    import random
    daily_affirmation = random.choice(affirmations)
    
    stats = {
        'total_entries': total_entries,
        'current_streak': streak,
        'most_common_mood': most_common_mood.title(),
        'days_active': days_active
    }
    
    # Prepare chart data
    chart_dates = []
    chart_moods = []
    chart_activity = []
    
    # Sort for chart (oldest to newest)
    for p in sorted(progress_data, key=lambda x: x.date):
        chart_dates.append(p.date.strftime('%b %d'))
        chart_moods.append(p.mood_score or 0)
        chart_activity.append(p.activity_score or 0)
        
    chart_data = {
        'labels': chart_dates,
        'moods': chart_moods,
        'activity': chart_activity
    }
    
    return render_template('dashboard.html', 
                         entries=recent_entries,
                         progress=progress_data,
                         affirmation=daily_affirmation,
                         stats=stats,
                         chart_data=chart_data)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint with dynamic suggestions"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    user_input = data.get('text', '')
    mood = analyze_mood(user_input)
    
    # Context-aware suggestions based on mood
    suggestions = {
        'improving': [
            'Celebrate this win - write down 3 things you did well',
            'Share your positivity with a friend or in the community',
            'Set a new goal while you are feeling strong'
        ],
        'struggling': [
            'Be gentle with yourself, healing is non-linear',
            'Try the 5-minute box breathing exercise now',
            'Write a letter to yourself offering compassion'
        ],
        'neutral': [
            'Take a moment to identify one small joy today',
            'Go for a short walk to clear your mind',
            'Practice mindfulness for 5 minutes'
        ],
        'crisis': [
            'Please reach out for help immediately - you are not alone.',
            'Call Vandrevala Foundation (India): 1860-266-2345 (24/7)',
            'Call iCall Helpline: 9152987821 (Mon-Sat, 8 AM - 10 PM)'
        ]
    }
    
    # Update user's recovery stage if significant
    if mood != 'neutral' and mood != 'crisis':
        current_user.recovery_stage = mood
        db.session.commit()
    
    return jsonify({
        'mood': mood if mood != 'crisis' else 'Support Needed',
        'message': 'Analysis complete',
        'next_steps': suggestions.get(mood, suggestions['neutral'])
    })

@app.route('/generate_plan', methods=['GET', 'POST'])
def generate_plan():
    """Generate recovery plan with AI - optimized for speed"""
    global RATE_LIMITED, RATE_LIMIT_RESET_TIME
    
    # Ensure user is available for context if needed
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    user_input = request.form.get('user_input', '')
    plan_type = request.form.get('plan_type', '7day')
    
    if not user_input:
        flash('Please describe your situation', 'error')
        return redirect(url_for('index'))
    
    groq_key = app.config['GROQ_API_KEY']
    if not groq_key:
        flash('API key not configured', 'error')
        return redirect(url_for('index'))
    
    # Fallback responses for when API is rate-limited
    def get_fallback_responses(situation_text, plan_duration):
        return {
            'therapist': f"""I understand you're going through a difficult time. Based on what you've shared, here are some compassionate insights:

**Validation of Your Feelings:**
Your emotions are completely valid. Breakups and emotional challenges are among life's most difficult experiences, and it's okay to feel overwhelmed.

**What You're Experiencing:**
- It's normal to have good days and bad days
- Healing is not linear - there will be ups and downs
- Your feelings may change from hour to hour, and that's okay

**Immediate Support:**
1. **Practice Self-Compassion**: Treat yourself with the same kindness you'd offer a close friend
2. **Allow Yourself to Grieve**: Don't rush the process
3. **Maintain Routine**: Small daily structures can provide stability
4. **Reach Out**: Connect with trusted friends or family when you feel ready

**Remember:** You are stronger than you think, and this pain is temporary. Every day you get through is a step forward in your healing journey.

*If you're experiencing severe distress, please reach out to a mental health professional or call a helpline.*""",
            
            'planner': f"""**Your {plan_duration.upper()} Recovery Action Plan**

**Week 1: Foundation & Self-Care**
- Day 1-2: Allow yourself to feel and process emotions
- Day 3-4: Establish a simple daily routine (sleep, meals, hygiene)
- Day 5-7: Start journaling 10 minutes daily
- Daily: Practice 5-minute breathing exercises

**Week 2: Rebuilding & Connection** (if applicable)
- Reconnect with one friend or family member
- Try one new activity or hobby
- Continue journaling - focus on gratitude
- Start light physical activity (walks, yoga)

**Daily Practices:**
✅ Morning: Set one small intention for the day
✅ Afternoon: Take a mindful break (5-10 minutes)
✅ Evening: Journal or reflect on one positive moment
✅ Night: Practice relaxation before bed

**Self-Care Checklist:**
- [ ] Drink 6-8 glasses of water daily
- [ ] Eat nutritious meals
- [ ] Get 7-8 hours of sleep
- [ ] Limit social media exposure
- [ ] Engage in one enjoyable activity

**Progress Markers:**
You'll know you're healing when:
- You have more good moments than bad
- You can think about the future with hope
- You're rediscovering your interests
- You feel more like yourself

*Adjust this plan to your pace. Healing isn't a race.*""",
            
            'closure': f"""**Finding Closure & Letting Go**

Closure is something you give yourself, not something you receive from others. Here's how to create it:

**Understanding Closure:**
Closure doesn't mean forgetting or not caring. It means accepting what happened and choosing to move forward.

**Letting Go Rituals:**

1. **The Letter You'll Never Send**
   - Write everything you wish you could say
   - Be completely honest with your emotions
   - When finished, safely burn or shred it
   - This symbolizes releasing those feelings

2. **Memory Box Ritual**
   - Gather items that remind you of the relationship
   - Place them in a box
   - Store it away or donate/discard when ready
   - This creates physical distance

3. **Forgiveness Practice**
   - Forgive yourself for any perceived mistakes
   - Forgive them (this is for YOUR peace, not theirs)
   - Write: "I release you and I release myself"

**Reframing Your Story:**
Instead of "Why did this happen to me?"
Try: "What can I learn from this experience?"

**Signs You're Finding Closure:**
- You can think about them without intense pain
- You're not checking their social media
- You're excited about your own future
- You wish them well (even if from afar)

**Affirmation:**
"I am complete on my own. I honor what was, I accept what is, and I embrace what will be."

*Closure is a journey, not a destination. Be patient with yourself.*""",
            
            'honesty': f"""**Reality Check: The Honest Truth You Need**

Let's be real for a moment, because sometimes we need tough love:

**The Hard Truths:**
1. **They're Not Coming Back** - And that's actually okay. If they wanted to be with you, they would be. Stop waiting.

2. **Stalking Social Media Hurts YOU** - Every time you check their profile, you're reopening the wound. Block, mute, or delete. Your healing > your curiosity.

3. **You're Romanticizing the Past** - Your brain is playing highlight reels. Remember the bad times too. There's a reason it ended.

4. **No Contact Means NO CONTACT** - Not "just one text." Not "happy birthday." Not "I saw this and thought of you." NONE.

**What You Need to Do:**
- **Stop Making Excuses**: For them, for the relationship, for why you're still stuck
- **Delete the Number**: Yes, really. You have it memorized? Change your phone.
- **Unfollow Everywhere**: Instagram, Facebook, Twitter, LinkedIn - everywhere
- **Remove Reminders**: Photos, gifts, that hoodie - box it up or toss it

**The Brutal Reality:**
- They're probably not thinking about you as much as you're thinking about them
- Begging or pleading will NEVER work - it only pushes them further away
- You cannot "fix" this by being perfect - it's over, and that's final

**But Here's the GOOD News:**
- You're wasting energy on someone who doesn't want you when you could be finding someone who does
- Every day you spend healing is a day closer to being happy again
- You WILL love again, and it will be better because you'll know what you deserve

**Your Action Plan:**
1. Block/delete them TODAY
2. Tell your friends to stop updating you about them
3. Focus on YOU - gym, hobbies, career, friends
4. Give yourself 90 days of strict no contact
5. Watch how much better you feel

**Bottom Line:**
You deserve someone who chooses you every single day without hesitation. This person didn't. So stop choosing them. Choose yourself instead.

*This might sting now, but future you will thank you for reading this.*"""
        }
    
    # Check if we're currently rate-limited and should skip API calls
    if RATE_LIMITED and RATE_LIMIT_RESET_TIME:
        if datetime.now() < RATE_LIMIT_RESET_TIME:
            # Still rate-limited, use fallback immediately
            flash('⚠️ AI service is temporarily at capacity. Showing expertly crafted recovery guidance.', 'info')
            responses = get_fallback_responses(user_input, plan_type)
            session['last_responses'] = responses
            return render_template('results.html', responses=responses)
        else:
            # Reset time has passed, try API again
            RATE_LIMITED = False
            RATE_LIMIT_RESET_TIME = None
    
    # Try API calls with timeout protection
    use_fallback = False
    
    try:
        # Quick test: try to create agents (this is fast)
        therapist, closure, planner, honesty = create_agents(groq_key)
        
        # Generate responses with individual error handling and timeouts
        responses = {}
        fallback_data = get_fallback_responses(user_input, plan_type)
        
        # Try each agent separately with timeout (3 seconds max per agent)
        agents_config = [
            ('therapist', therapist, f"Situation: {user_input}"),
            ('planner', planner, f"Create a {plan_type} recovery plan for: {user_input}"),
            ('closure', closure, f"Situation: {user_input}"),
            ('honesty', honesty, f"Situation: {user_input}")
        ]
        
        import concurrent.futures
        import json as json_module
        
        def call_agent_with_timeout(agent_name, agent, prompt, timeout=6):
            """Call agent with timeout protection and error parsing"""
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(agent.run, prompt)
                    result = future.result(timeout=timeout)
                    
                    # Check if result.content is a JSON error
                    content = result.content
                    if isinstance(content, str):
                        # Try to parse as JSON to detect error responses
                        try:
                            parsed = json_module.loads(content)
                            if isinstance(parsed, dict) and 'error' in parsed:
                                # This is an error response
                                error_msg = parsed.get('error', {}).get('message', '')
                                return agent_name, None, error_msg
                        except (json_module.JSONDecodeError, ValueError):
                            # Not JSON, it's actual content
                            pass
                    
                    return agent_name, content, None
            except concurrent.futures.TimeoutError:
                return agent_name, None, "timeout"
            except Exception as e:
                error_str = str(e)
                # Try to extract error from exception message if it contains JSON
                try:
                    if '{' in error_str and 'error' in error_str:
                        # Extract JSON from error string
                        start = error_str.find('{')
                        end = error_str.rfind('}') + 1
                        if start != -1 and end > start:
                            json_str = error_str[start:end]
                            parsed = json_module.loads(json_str)
                            if 'error' in parsed:
                                error_msg = parsed['error'].get('message', error_str)
                                return agent_name, None, error_msg
                except:
                    pass
                return agent_name, None, error_str
        
        # Try all agents with timeout
        for agent_name, agent, prompt in agents_config:
            name, content, error = call_agent_with_timeout(agent_name, agent, prompt, timeout=6)
            
            if content:
                # Success! Validate it's not an error JSON
                if isinstance(content, str) and content.strip().startswith('{'):
                    try:
                        parsed = json_module.loads(content)
                        if 'error' in parsed:
                            # This is actually an error, use fallback
                            responses[agent_name] = fallback_data[agent_name]
                            use_fallback = True
                            RATE_LIMITED = True
                            RATE_LIMIT_RESET_TIME = datetime.now() + timedelta(hours=1)
                            continue
                    except:
                        pass
                
                # Valid content
                responses[agent_name] = content
            else:
                # Failed - check if it's a rate limit error
                if error:
                    error_str = error.lower()
                    is_rate_limit = any(keyword in error_str for keyword in [
                        'rate', 'limit', 'quota', 'exceeded', 'ratelimit', 
                        'tokens per day', 'tpd', '429', 'timeout'
                    ])
                    
                    if is_rate_limit and 'timeout' not in error_str:
                        # Mark as rate-limited globally
                        RATE_LIMITED = True
                        RATE_LIMIT_RESET_TIME = datetime.now() + timedelta(hours=1)
                
                # Use fallback for this agent
                responses[agent_name] = fallback_data[agent_name]
                use_fallback = True
        
        # Show info message if we used fallback
        if use_fallback:
            flash('⚠️ AI service is temporarily at capacity. Showing expertly crafted recovery guidance.', 'info')
        
        # Save to session for display
        session['last_responses'] = responses
        
        return render_template('results.html', responses=responses)
        
    except Exception as e:
        # If agent creation fails, use complete fallback immediately
        print(f"Global error in generate_plan: {str(e)}") # Log for debugging
        error_msg = str(e).lower()
        is_rate_limit = any(keyword in error_msg for keyword in [
            'rate', 'limit', 'quota', 'exceeded', 'ratelimit', 
            'tokens per day', 'tpd', '429'
        ])
        
        if is_rate_limit:
            # Mark as rate-limited globally
            RATE_LIMITED = True
            RATE_LIMIT_RESET_TIME = datetime.now() + timedelta(hours=1)
            flash('⚠️ AI service has reached daily limit. Showing expertly crafted recovery guidance.', 'warning')
        else:
            # For connection errors or other issues
            flash('⚠️ Showing expertly crafted recovery guidance (AI connection unavailable).', 'info')
        
        responses = get_fallback_responses(user_input, plan_type)
        session['last_responses'] = responses
        return render_template('results.html', responses=responses)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    """Digital journal with mood tracking"""
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        content = request.form.get('content')
        mood = request.form.get('mood', 'neutral')
        tags = request.form.get('tags', '')
        
        entry = JournalEntry(
            user_id=current_user.id,
            content=content,
            mood=mood,
            tags=tags
        )
        db.session.add(entry)
        
        # Update progress
        progress = Progress(
            user_id=current_user.id,
            mood_score={'happy': 8, 'neutral': 5, 'sad': 3}.get(mood, 5),
            activity_score=6,
            social_score=5
        )
        db.session.add(progress)
        db.session.commit()
        
        flash('Journal entry saved!', 'success')
        return redirect(url_for('journal'))
    
    entries = JournalEntry.query.filter_by(user_id=current_user.id)\
        .order_by(JournalEntry.created_at.desc()).all()
    
    return render_template('journal.html', entries=entries)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    """Delete a journal entry"""
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Unauthorized action', 'error')
        return redirect(url_for('journal'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted successfully', 'success')
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/resources')
def resources():
    """Indian-specific resources page with comprehensive information"""
    resources_data = {
        'helplines': [
            {
                'name': 'Vandrevala Foundation',
                'type': '24/7 Helpline',
                'contact': '1860-266-2345',
                'website': 'https://www.vandrevalafoundation.com',
                'description': 'Free mental health support and counseling',
                'available': '24/7'
            },
            {
                'name': 'iCall Psychosocial Helpline',
                'type': 'Counseling',
                'contact': '9152987821',
                'website': 'https://icallhelpline.org',
                'description': 'Professional counseling services',
                'available': 'Mon-Sat, 8 AM - 10 PM'
            },
            {
                'name': 'AASRA',
                'type': 'Crisis Helpline',
                'contact': '91-9820466726',
                'website': 'http://www.aasra.info',
                'description': '24/7 crisis intervention',
                'available': '24/7'
            }
        ],
        'online_therapy': [
            {
                'name': 'The Mind Clan',
                'type': 'Online Therapy Platform',
                'website': 'https://themindclan.com',
                'description': 'Affordable online therapy with licensed professionals',
                'pricing': 'Starting ₹500/session'
            },
            {
                'name': 'YourDOST',
                'type': 'Emotional Support',
                'website': 'https://yourdost.com',
                'description': 'Chat-based emotional wellness platform',
                'pricing': 'Free & Paid options'
            },
            {
                'name': 'BetterHelp India',
                'type': 'Online Counseling',
                'website': 'https://www.betterhelp.com',
                'description': 'International platform with Indian therapists',
                'pricing': 'Starting $60/week'
            }
        ],
        'self_help': [
            {
                'name': 'Headspace',
                'type': 'Meditation App',
                'description': 'Guided meditation and mindfulness',
                'icon': 'fa-brain'
            },
            {
                'name': 'Calm',
                'type': 'Sleep & Meditation',
                'description': 'Sleep stories and relaxation techniques',
                'icon': 'fa-moon'
            },
            {
                'name': 'Journaling',
                'type': 'Self-Reflection',
                'description': 'Use our built-in journal feature',
                'icon': 'fa-book'
            }
        ]
    }
    
    return render_template('resources.html', resources=resources_data)

@app.route('/community')
def community():
    """Support community forum with dynamic content"""
    from datetime import datetime, timedelta
    import random
    
    # Generate dynamic community stats
    community_stats = {
        'total_members': random.randint(4500, 5500),
        'posts_today': random.randint(15, 45),
        'active_now': random.randint(50, 150),
        'success_stories': random.randint(200, 300)
    }
    
    # Sample posts (in production, these would come from database)
    sample_posts = [
        {
            'id': 1,
            'author': 'Priya M.',
            'time_ago': '2 hours ago',
            'category': 'success',
            'content': 'It\'s been 3 months since my breakup, and I can finally say I\'m happy again! This community and the AI tools helped me so much. To anyone struggling: it gets better, I promise. 💪',
            'hearts': 45,
            'hugs': 23,
            'comments': 12
        },
        {
            'id': 2,
            'author': 'Rahul K.',
            'time_ago': '5 hours ago',
            'category': 'advice',
            'content': 'How do you deal with seeing your ex on social media? I know I should unfollow but I can\'t bring myself to do it. Any advice?',
            'hearts': 18,
            'hugs': 34,
            'comments': 28
        },
        {
            'id': 3,
            'author': 'Ananya S.',
            'time_ago': '8 hours ago',
            'category': 'support',
            'content': 'Today marks one month. Some days are harder than others, but I\'m learning to be okay with not being okay. Thank you all for being here.',
            'hearts': 67,
            'hugs': 89,
            'comments': 19
        },
        {
            'id': 4,
            'author': 'Vikram P.',
            'time_ago': '12 hours ago',
            'category': 'general',
            'content': 'Just wanted to share that I went out with friends for the first time in weeks. Baby steps, but it felt good to laugh again.',
            'hearts': 52,
            'hugs': 41,
            'comments': 15
        },
        {
            'id': 5,
            'author': 'Meera D.',
            'time_ago': '1 day ago',
            'category': 'resources',
            'content': 'Found this amazing meditation app that\'s been helping with anxiety. DM me if you want the name. Also, the breathing exercise on this platform is a lifesaver!',
            'hearts': 38,
            'hugs': 22,
            'comments': 31
        },
        {
            'id': 6,
            'author': 'Arjun T.',
            'time_ago': '1 day ago',
            'category': 'advice',
            'content': 'Is it normal to still miss them even when you know the relationship was toxic? I feel so conflicted.',
            'hearts': 42,
            'hugs': 58,
            'comments': 24
        }
    ]
    
    # Top contributors
    top_contributors = [
        {'name': 'Kavya R.', 'posts': 47, 'hearts': 892},
        {'name': 'Aditya M.', 'posts': 39, 'hearts': 756},
        {'name': 'Shreya K.', 'posts': 35, 'hearts': 634},
        {'name': 'Rohan S.', 'posts': 28, 'hearts': 521},
        {'name': 'Nisha P.', 'posts': 24, 'hearts': 489}
    ]
    
    return render_template('community.html', 
                         community_stats=community_stats,
                         posts=sample_posts,
                         top_contributors=top_contributors)

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    from datetime import datetime
    return render_template('privacy.html', current_date=datetime.now().strftime('%B %d, %Y'))

@app.route('/terms')
def terms():
    """Terms of Service page"""
    from datetime import datetime
    return render_template('terms.html', current_date=datetime.now().strftime('%B %d, %Y'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Us page"""
    if request.method == 'POST':
        data = request.get_json()
        # In production, you'd send an email or save to database
        # For now, just acknowledge receipt
        flash('Thank you for contacting us! We\'ll respond within 24 hours.', 'success')
        return jsonify({'status': 'success', 'message': 'Message received'})
    
    return render_template('contact.html')

@app.template_filter('markdown')
def markdown_filter(text):
    if not text:
        return ""
    return markdown2.markdown(text, extras=["fenced-code-blocks", "tables", "strike", "underline"])

# ------------------------------
# Initialize Database
# ------------------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)