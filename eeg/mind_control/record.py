import uuid
from mind_control.supabase import supabase

def start_focus_session():
    session_id = str(uuid.uuid4())
    return session_id

def save_eeg_data(session_id, eeg_data, metrics_list):
    response = supabase.table('focus_sessions').insert({
        'session_id': session_id,
        'eeg_data': eeg_data,
        "metrics": metrics_list
    }).execute()
    return response