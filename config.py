from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in .env file")