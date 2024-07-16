import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# test connection
def save_data_to_supabase(data, prediction):
    response = supabase.table('eeg_data').insert({
        'data': data,
        'prediction': prediction
    }).execute()
    return response
