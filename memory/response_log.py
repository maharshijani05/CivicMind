# memory/response_log.py

from datetime import datetime

response_log = []

def log_response(agent, text):
    response_log.append({
        "agent": agent,
        "text": text,
        "timestamp": datetime.now().isoformat()
    })

def get_all_logs():
    return response_log

def clear_logs():
    response_log.clear()
