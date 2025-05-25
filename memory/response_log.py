# memory/response_log.py

from datetime import datetime

response_log = []

def log_response(agent, text,round_num=None):
    response_log.append({
        "agent": agent,
        "text": text,
        "timestamp": datetime.now().isoformat(),
        "round_num": round_num
    })

def get_all_logs():
    return response_log

def clear_logs():
    response_log.clear()
