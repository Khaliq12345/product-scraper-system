from dotenv import load_dotenv
import os

load_dotenv()


SUPABSE_URL = os.getenv("SUPABSE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY", "")