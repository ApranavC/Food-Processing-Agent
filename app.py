import streamlit as st
import os
import subprocess
import sys
from agent import run_agent_query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Page configuration
st.set_page_config(
    page_title="Food Agent AI",
    page_icon="🌾", # Keep this as it's the official brand icon, or remove if user wants NO emojis
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
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='header'>Intelligent Food Agent</h1>", unsafe_allow_html=True)

# Determine available providers based on API keys
available_providers = []
if os.getenv("OPENAI_API_KEY"):
    available_providers.append("OpenAI")
if os.getenv("GOOGLE_API_KEY"):
    available_providers.append("Google Gemini")
if os.getenv("GROQ_API_KEY"):
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
query = st.text_input("Ask a question about food processing infrastructure:")

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
st.caption("Powered by MoFPI Data, LangChain, and Streamlit.")
