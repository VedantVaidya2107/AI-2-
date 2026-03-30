import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_KEY")


supabase: Client = None

if url and key:
    try:
        supabase = create_client(url, key)
        # Check if it's a service key or anon key
        is_service = "service_role" in (key[:100] if key else "") or "service" in (key.lower() if key else "")
        role_label = "SERVICE_ROLE" if is_service else "ANON"
        print(f"[Supabase] Client initialized with {role_label} key.")
    except Exception as e:
        print(f"[Supabase Error] Failed to initialize: {e}")
else:
    print("[Supabase Warning] Missing SUPABASE_URL or SUPABASE_ANON_KEY.")

def ensure_supabase():
    if supabase is None:
        raise Exception("Supabase client not initialized. Please check environment variables.")
    return supabase
