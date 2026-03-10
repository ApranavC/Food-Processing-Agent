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
    page_title="🌾 Food Agent AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
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
        padding: 20px;
    }
    .chat-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='header'>🌾 Intelligent Food Processing Infrastructure Agent</h1>", unsafe_allow_html=True)
st.write("Welcome! This AI assistant helps you navigate government schemes, find cold storage facilities, and explore crop processing opportunities based on MoFPI data.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    provider = st.radio("Select AI Provider", ["OpenAI", "Google Gemini", "Groq"], index=1)
    
    if provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        model_name = st.selectbox("Select OpenAI Model", ["gpt-4o", "gpt-4o-mini"], index=0)
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    elif provider == "Google Gemini":
        api_key = st.text_input("Google AI Studio API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
        model_name = st.selectbox("Select Gemini Model", [
            "models/gemini-2.0-flash", 
            "models/gemini-3-flash-preview", 
            "models/gemini-3-pro-preview",
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro"
        ], index=1)
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
    else: # Groq
        api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
        model_name = st.selectbox("Select Groq Model", [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3.2-11b-text-preview",
            "mixtral-8x7b-32768"
        ], index=0)
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            
    if api_key:
        st.success(f"{provider} API Key updated!")
    else:
        st.info(f"Please enter your {provider} API Key to proceed.")
        if provider == "Google Gemini":
            st.markdown("[Get a free Gemini API Key here](https://aistudio.google.com/app/apikey)")

    st.markdown("---")
    st.subheader("Capabilities")
    st.markdown("""
    - 🔍 Search Government Schemes
    - ❄️ Locate Cold Storage Projects
    - 📈 Analyze Crop Production
    - 💡 Get Recommendations
    """)

# Main Chat Interface
query = st.text_input("Ask a question (e.g., 'What schemes are available for potato processing in Punjab?'):")

if st.button("Query AI Agent"):
    if not api_key:
        st.error(f"Please provide an {provider} API Key in the sidebar.")
    elif query:
        with st.spinner(f"🧠 {provider} Agent is thinking using {model_name}..."):
            try:
                response = run_agent_query(query, provider=provider, model_name=model_name, api_key=api_key)
                st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
                st.subheader(f"💡 {provider} Recommendation")
                st.write(response)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query.")

# Footer
st.markdown("---")
st.caption("Powered by MoFPI Data, LangChain, and Streamlit. Built for rural entrepreneurs and farmers.")
