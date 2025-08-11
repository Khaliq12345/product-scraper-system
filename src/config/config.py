from dotenv import load_dotenv
import os

load_dotenv()
SUPABSE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY", "")