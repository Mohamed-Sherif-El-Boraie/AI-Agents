from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = os.getenv("GROQ_URL")
MODEL_NAME = os.getenv("MODEL_NAME")



if TAVILY_API_KEY is None:
    raise EnvironmentError("TAVILY_API_KEY not set in .env file")
if GROQ_API_KEY is None:
    raise EnvironmentError("GROQ_API_KEY not set in .env file")
if GROQ_URL is None:
    raise EnvironmentError("GROQ_URL not set in .env file")
if MODEL_NAME is None:
    raise EnvironmentError("MODEL_NAME not set in .env file")