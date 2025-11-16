import streamlit as st
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import json
import pytz
from setup import *
from llm_service import *

# Page config
st.set_page_config(
    page_title="Mood Check-in",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .checkin-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .insight-card {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        border: 2px solid #4CAF50;
    }
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .auth-container {
        max-width: 500px;
        margin: 5rem auto;
        padding: 3rem;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
    }
    h2, h3 {
        color: #34495e;
    }
    .stMultiSelect {
        margin-bottom: 1rem;
    }
    .logout-btn button {
        background-color: #f44336 !important;
    }
    .logout-btn button:hover {
        background-color: #da190b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_timezone' not in st.session_state:
    st.session_state.user_timezone = None
if 'checkins' not in st.session_state:
    st.session_state.checkins = []
if 'latest_insights' not in st.session_state:
    st.session_state.latest_insights = None
if 'loading' not in st.session_state:
    st.session_state.loading = False


# Async wrapper for Streamlit
def run_async(coro):
    """Run async function in Streamlit's synchronous context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# Auth Functions - INTEGRATED WITH SUPABASE
# TODO: Import your SUPABASE client at the top of the file
# from your_module import SUPABASE
import uuid

def check_username_exists(username: str) -> bool:
    """Check if username already exists in database"""
    try:
        response = SUPABASE.table("users").select("username").eq("username", username).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking username: {e}")
        st.error(f"Database error: {e}")
        return True  # Fail safe - assume exists to prevent duplicate attempts


def register_user(username: str, timezone: str) -> Dict[str, Any]:
    """Register a new user in the database"""
    try:
        user_data = {
            "user_id": str(uuid.uuid4()),  # Generate UUID
            "username": username,
            "timezone_user": timezone
        }
        response = SUPABASE.table("users").insert(user_data).execute()
        
        if not response.data or len(response.data) == 0:
            raise Exception("Failed to create user - no data returned")
        
        return response.data[0]
    except Exception as e:
        print(f"Error registering user: {e}")
        raise Exception(f"Registration failed: {str(e)}")


def login_user(username: str) -> Dict[str, Any]:
    """Login user by fetching their data from database"""
    try:
        response = SUPABASE.table("users").select("*").eq("username", username).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        return None  # User not found
    except Exception as e:
        print(f"Error logging in user: {e}")
        st.error(f"Login error: {e}")
        return None


# Mock function - replace with your actual implementation
async def generate_insights(request_data: GenerateInsightsRequest, user_timezone: str, user_id: str):
    """
    Replace this with your actual generate_insights function
    This is a placeholder that simulates the API call
    """
    # Simulate API delay
    # await asyncio.sleep(1)
    
    request = GenerateInsightsRequest(**request_data)
    
    print("request_data: ", request_data)
    Daily_Action = await LLM_Query(request, user_id ,user_timezone)
    return Daily_Action

  


# Mock function for fetching check-ins
@st.cache_data(ttl=60)
def fetch_checkins(user_id: str) -> List[Dict]:
    """
    Replace with your actual Supabase query:
    response = SUPABASE.table("mood_checkIns")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .limit(10)\
        .execute()
    return response.data
    """
    # Mock data - replace with actual DB call
    return []


def get_timezone_options() -> List[str]:
    """Get all available timezones grouped by region"""
    return pytz.all_timezones


def display_checkin_card(checkin: Dict, index: int):
    """Display a single check-in in a nice card format"""
    st.markdown(f"""
        <div class="checkin-card">
            <h4>Check-in #{index + 1} • {checkin.get('timestamp', 'Just now')}</h4>
            <p><strong>Feelings:</strong> {', '.join(checkin.get('feelings', []))}</p>
            <p><strong>Energy Level:</strong> {checkin.get('energy_value', 0)}/10</p>
            <p><strong>Emotional Intelligence:</strong> {checkin.get('emotionalIntelligenceQuestion', 'N/A')}</p>
            <p><strong>Mirror Reflection:</strong> {checkin.get('mirrorQuestion', 'N/A')}</p>
        </div>
    """, unsafe_allow_html=True)


def display_insights(insights: Dict):
    """Display insights in a beautiful card"""
    if not insights:
        return
    
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Your Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Overall Mood**")
        st.info(insights.get('overall_mood', 'N/A'))
        
        st.markdown(f"**Pattern Noticed**")
        st.success(insights.get('pattern_noticed', 'N/A'))
        
        st.markdown(f"**Mood Trend**")
        st.warning(insights.get('mood_trend', 'N/A'))
    
    with col2:
        st.markdown(f"**Comparison Insight**")
        st.info(insights.get('comparison_insight', 'N/A'))
        
        st.markdown(f"**Suggestions**")
        st.success(insights.get('suggestions', 'N/A'))
    
    st.markdown('</div>', unsafe_allow_html=True)


def auth_page():
    """Login/Register page"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.title("🧠 Mood Check-in Tracker")
    st.markdown("### Welcome! Please login or register to continue")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("#### Login to your account")
        with st.form("login_form"):
            login_username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )
            
            login_submit = st.form_submit_button("🔓 Login")
            
            if login_submit:
                if not login_username:
                    st.error("Please enter a username!")
                else:
                    # Check if user exists
                    user = login_user(login_username)
                    
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user['user_id']  # Changed from 'id' to 'user_id'
                        st.session_state.username = user['username']
                        st.session_state.user_timezone = user['timezone_user']
                        
                        # Load existing check-ins
                        st.session_state.checkins = fetch_checkins(user['user_id'])
                        
                        st.success(f"Welcome back, {login_username}!")
                        st.rerun()
                    else:
                        st.error("Username not found. Please register first!")
    
    with tab2:
        st.markdown("#### Create a new account")
        with st.form("register_form"):
            reg_username = st.text_input(
                "Username",
                placeholder="Choose a unique username",
                key="reg_username",
                help="This must be unique across all users"
            )
            
            # Timezone selection with search
            timezone_options = get_timezone_options()
            
            # Group common timezones at the top
            popular_timezones = [
                "Asia/Manila",
                "Asia/Tokyo",
                "Asia/Singapore",
                "America/New_York",
                "America/Los_Angeles",
                "Europe/London",
                "Australia/Sydney"
            ]
            
            st.markdown("**Select Your Timezone**")
            
            # Radio for popular or search all
            timezone_choice = st.radio(
                "Choose selection method:",
                ["Popular Timezones", "Search All Timezones"],
                key="timezone_choice",
                horizontal=True
            )
            
            if timezone_choice == "Popular Timezones":
                selected_timezone = st.selectbox(
                    "Select timezone",
                    options=popular_timezones,
                    key="popular_tz"
                )
            else:
                selected_timezone = st.selectbox(
                    "Search and select timezone",
                    options=timezone_options,
                    index=timezone_options.index("Asia/Manila") if "Asia/Manila" in timezone_options else 0,
                    key="all_tz",
                    help="Type to search for your timezone"
                )
            
            # Show current time in selected timezone
            if selected_timezone:
                tz = pytz.timezone(selected_timezone)
                current_time = datetime.now(tz).strftime("%I:%M %p, %B %d, %Y")
                st.info(f"🕐 Current time in {selected_timezone}: **{current_time}**")
            
            register_submit = st.form_submit_button("✅ Register")
            
            if register_submit:
                if not reg_username:
                    st.error("Please enter a username!")
                elif len(reg_username) < 3:
                    st.error("Username must be at least 3 characters long!")
                elif not selected_timezone:
                    st.error("Please select a timezone!")
                else:
                    # Check if username exists
                    if check_username_exists(reg_username):
                        st.error("❌ Username is already taken! Please choose another one.")
                    else:
                        # Register new user
                        try:
                            user = register_user(reg_username, selected_timezone)
                            st.session_state.authenticated = True
                            st.session_state.user_id = user['user_id']  # Changed from 'id' to 'user_id'
                            st.session_state.username = user['username']
                            st.session_state.user_timezone = user['timezone_user']
                            
                            # Initialize empty check-ins for new user
                            st.session_state.checkins = []
                            
                            st.success(f"✅ Account created successfully! Welcome, {reg_username}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def main_app():
    """Main application after authentication"""
    # Header with user info and logout
    col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
    
    with col_header1:
        st.title("🧠 Mood Check-in Tracker")
    
    with col_header2:
        st.metric("User", st.session_state.username)
    
    with col_header3:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.user_timezone = None
            st.session_state.checkins = []
            st.session_state.latest_insights = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.caption(f"🌍 Timezone: {st.session_state.user_timezone}")
    st.markdown("---")
    
    # Left column: Check-in form
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.header("📝 New Check-in")
        
        with st.form("checkin_form", clear_on_submit=True):
            # Feelings multi-select
            feelings_options = [
                "happy", "sad", "anxious", "excited", "tired", 
                "energetic", "calm", "stressed", "grateful", 
                "frustrated", "hopeful", "overwhelmed"
            ]
            feelings = st.multiselect(
                "How are you feeling today?",
                options=feelings_options,
                placeholder="Select all that apply..."
            )
            
            # Energy slider
            energy_value = st.slider(
                "Energy Level",
                min_value=1,
                max_value=10,
                value=5,
                help="Rate your energy from 1 (exhausted) to 10 (fully energized)"
            )
            
            # Emotional Intelligence question
            ei_question = st.text_area(
                "Emotional Intelligence",
                placeholder="What emotions are you avoiding right now? How is it limiting your potential?",
                height=100
            )
            
            # Mirror question
            mirror_question = st.text_area(
                "Mirror Question",
                placeholder="What would you tell someone else facing this exact situation?",
                height=100
            )
            
            # Submit button
            submitted = st.form_submit_button("✅ Submit Check-in")
            
            if submitted:
                if not feelings:
                    st.error("Please select at least one feeling!")
                elif not ei_question or not mirror_question:
                    st.error("Please answer both reflection questions!")
                else:
                    # Create check-in object
                    new_checkin = {
                        "feelings": feelings,
                        "energy_value": energy_value,
                        "emotionalIntelligenceQuestion": ei_question,
                        "mirrorQuestion": mirror_question,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Add to session state
                    st.session_state.checkins.insert(0, new_checkin)
                    
                    # TODO: Save to database here
                    # save_checkin_to_db(st.session_state.user_id, new_checkin)
                    
                    st.success("✅ Check-in submitted successfully!")
                    st.rerun()
    
    with col_right:
        st.header("📊 Your Check-ins")
        
        if st.session_state.checkins:
            st.metric(
                label="Total Check-ins",
                value=len(st.session_state.checkins),
                delta=f"Energy: {st.session_state.checkins[0].get('energy_value', 0)}/10"
            )
            
            # Display recent check-ins
            st.markdown("### Recent Check-ins")
            for idx, checkin in enumerate(st.session_state.checkins[:5]):  # Show last 5
                display_checkin_card(checkin, idx)
        else:
            st.info("No check-ins yet. Submit your first one to get started!")
    
    # Generate Insights Section
    st.markdown("---")
    st.header("🎯 Generate Insights")
    
    if st.session_state.checkins:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔮 Generate AI Insights", disabled=st.session_state.loading):
                st.session_state.loading = True
                
                with st.spinner("🧠 Analyzing your patterns..."):
                    try:
                        # Get latest check-in
                        latest_checkin = st.session_state.checkins[0]
                        
                        # Call your async function
                        insights = run_async(
                            generate_insights(
                                latest_checkin,
                                st.session_state.user_timezone,
                                st.session_state.user_id
                            )
                        )
                        
                        st.session_state.latest_insights = insights
                        st.session_state.loading = False
                        st.success("✨ Insights generated!")
                        st.rerun()
                        
                    except Exception as e:
                        st.session_state.loading = False
                        st.error(f"Error generating insights: {str(e)}")
        
        # Display insights if available
        if st.session_state.latest_insights:
            st.markdown("---")
            display_insights(st.session_state.latest_insights)
    else:
        st.warning("⚠️ Submit at least one check-in before generating insights!")
    
    # Footer
    st.markdown("---")
    st.caption("💡 Tip: Check in daily for more accurate insights and patterns!")


# Main routing logic
if not st.session_state.authenticated:
    auth_page()
else:
    main_app()