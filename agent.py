import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def get_agent(provider="OpenAI", model_name=None, api_key=None):
    # Use SQLite database created by Django
    db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    if provider == "Google Gemini":
        if not api_key:
            api_key = os.getenv("GOOGLE_API_KEY")
        # Default to gemini-2.0-flash if no model_name provided
        if not model_name:
            model_name = "gemini-2.0-flash"
        llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0)
    elif provider == "Groq":
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")
        # Default to llama-3.3-70b-versatile for Groq
        if not model_name:
            model_name = "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, groq_api_key=api_key, temperature=0)
    else:
        # Default to OpenAI
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        # Default to gpt-4o if no model_name provided
        if not model_name:
            model_name = "gpt-4o"
        llm = ChatOpenAI(model=model_name, openai_api_key=api_key, temperature=0)
    
    # Create the SQL agent
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools" if provider == "OpenAI" else "tool-calling", verbose=True)
    
    return agent_executor

def run_agent_query(query: str, provider="OpenAI", model_name=None, api_key=None):
    agent = get_agent(provider=provider, model_name=model_name, api_key=api_key)
    # Standard query for LangChain agent executor
    response = agent.invoke({"input": query})
    return response["output"]

if __name__ == "__main__":
    # Test query
    try:
        example_query = "What schemes are available for farmers and what are their benefits?"
        print(f"Query: {example_query}")
        # Default test with OpenAI (requires key)
        # print("Response:", run_agent_query(example_query))
    except Exception as e:
        print(f"Error running agent: {e}")
