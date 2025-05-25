from memory.response_log import get_all_logs

def get_last_agent_to_respond(current_agent, round_num):
    logs = get_all_logs()
    # Filter responses only from this round and before current agent speaks
    prior_responses_new = [
        log for log in logs 
        if log["round_num"] == round_num and log["agent"] != current_agent
    ]
    
    if not prior_responses_new:
        return None, None
    
    last_entry = prior_responses_new[-1]
    return last_entry["agent"], last_entry["text"]