import streamlit as st
import os
import subprocess
import sys
from agent import run_agent_query
from dotenv import load_dotenv, dotenv_values

# Load environment variables with override to ensure .env takes precedence
load_dotenv(override=True)

# Get keys explicitly defined in .env to prevent shell environment leakage
ENV_CONFIG = dotenv_values(".env")

# Debug: Print detected keys (masked) to terminal for troubleshooting
print(f"--- Environment Detection ---")
print(f"Detected OPENAI_API_KEY: {'Yes (Active)' if os.getenv('OPENAI_API_KEY') else 'No'}")
print(f"Detected GOOGLE_API_KEY: {'Yes (Active)' if os.getenv('GOOGLE_API_KEY') else 'No'}")
print(f"Detected GROQ_API_KEY: {'Yes (Active)' if os.getenv('GROQ_API_KEY') else 'No'}")
print(f"-----------------------------")

# Auto-initialize database for Cloud deployment
def init_db():
    db_path = os.path.join(os.getcwd(), "db.sqlite3")
    if not os.path.exists(db_path):
        st.info("Initializing database for the first time...")
        # Run migrations
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        # Seed data
        subprocess.run([sys.executable, "ingest_data.py"], check=True)
        st.success("Database initialized!")

init_db()

def validate_key(key):
    """Helper to check if a key is a real key and not a placeholder or empty."""
    if not key:
        return False
    # Remove markers of common placeholders or comments
    key = key.strip()
    if key in ["", "...", "your_key_here", "your_openai_key_here", "your_google_key_here", "your_groq_key_here"]:
        return False
    if len(key) < 20: # All real keys from these providers are long
        return False
    return True

# Page configuration
st.set_page_config(
    page_title="Food Agent AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .header {
        color: #1b5e20;
        text-align: center;
        padding: 10px 0;
        margin-bottom: 0;
    }
    .chat-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .config-row {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stDeployButton {
        display:none;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDecoration"] {
        display:none;
    }
    div[data-testid="stStatusWidget"] {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='header'>Intelligent Food Agent</h1>", unsafe_allow_html=True)

# Determine available providers based on API keys
# We check ENV_CONFIG to ensure we respect the .env file strictly when running locally
available_providers = []

openai_key = os.getenv("OPENAI_API_KEY")
if validate_key(openai_key):
    if not os.path.exists(".env") or "OPENAI_API_KEY" in ENV_CONFIG:
        available_providers.append("OpenAI")
    
google_key = os.getenv("GOOGLE_API_KEY")
if validate_key(google_key):
    # Only show Gemini if it's explicitly in .env (if .env exists)
    if not os.path.exists(".env") or "GOOGLE_API_KEY" in ENV_CONFIG:
        available_providers.append("Google Gemini")
    
groq_key = os.getenv("GROQ_API_KEY")
if validate_key(groq_key):
    if not os.path.exists(".env") or "GROQ_API_KEY" in ENV_CONFIG:
        available_providers.append("Groq")

# Fallback if no keys are found
if not available_providers:
    st.error("No API keys found in environment. Please configure your .env file or Streamlit Secrets.")
    st.stop()

# Provider and Model Selection in the main area
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        provider = st.selectbox("LLM Provider", available_providers, index=0)
    with col2:
        if provider == "OpenAI":
            model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=0)
            api_key = os.getenv("OPENAI_API_KEY")
        elif provider == "Google Gemini":
            model_name = st.selectbox("Model", [
                "models/gemini-2.0-flash", 
                "models/gemini-3-flash-preview", 
                "models/gemini-3-pro-preview",
                "models/gemini-1.5-flash",
                "models/gemini-1.5-pro"
            ], index=1)
            api_key = os.getenv("GOOGLE_API_KEY")
        else: # Groq
            model_name = st.selectbox("Model", [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "llama-3.2-11b-text-preview",
                "mixtral-8x7b-32768"
            ], index=0)
            api_key = os.getenv("GROQ_API_KEY")

# Main Chat Interface
st.markdown("---")

# Suggested Questions Expander
with st.expander("Suggested Questions"):
    st.write("""
    1. **What is the potato production in Ludhiana, Punjab for the year 2023-24?**
    2. **How many MT of tomato were produced in Pune, Maharashtra in 2023-24?**
    3. **Show me all operational cold storage projects in Maharashtra.**
    4. **List cold storage projects in Ludhiana, Punjab.**
    5. **What are the benefits of the Mega Food Park Scheme?**
    6. **Who is eligible for the PMKSY scheme?**
    7. **What is the application process for the CEFPPC scheme?**
    8. **Tell me about the Maharashtra Cold Chain Hub project.**
    9. **What is the capacity of the Punjab Apple Store?**
    10. **Show me schemes offered by the Ministry of Food Processing Industries.**
    """)

query = st.text_input("Ask a question about food processing infrastructure:", placeholder="e.g., Show me cold storage projects in Maharashtra")

if st.button("Run Query"):
    if query:
        with st.spinner(f"Agent is processing your request using {model_name}..."):
            try:
                response = run_agent_query(query, provider=provider, model_name=model_name, api_key=api_key)
                st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
                st.subheader(f"System Recommendation")
                st.write(response)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query.")

# Footer
st.markdown("---")
