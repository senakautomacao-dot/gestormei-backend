# core/supabase_client.py
import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE", "")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise RuntimeError("SUPABASE_URL ou SUPABASE_SERVICE_ROLE não configurados")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)
