import os

from dotenv import load_dotenv
from supabase import create_client


# ==================================
# LOAD ENVIRONMENT VARIABLES
# ==================================

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# ==================================
# VALIDATE CREDENTIALS
# ==================================

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing.")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing.")


# ==================================
# CREATE SUPABASE CLIENT
# ==================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==================================
# SAVE CHANGE EVENT
# ==================================

def save_change_event(change):

    data = {
        "event_type": change["type"],
        "object_name": change["object"],
        "track_id": change.get("track_id"),
        "confidence": change.get("confidence"),
        "previous_position": change.get(
            "previous_position"
        ),
        "current_position": change.get(
            "current_position"
        ) or change.get("position"),
        "distance": change.get(
            "distance"
        )
    }


    response = (
        supabase
        .table("change_events")
        .insert(data)
        .execute()
    )


    return response