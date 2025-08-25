from dotenv import load_dotenv
import os

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_KEY", "")
ENV = os.getenv("ENV", "dev")
OPENAI_KEY = os.getenv("OPENAI_KEY")
