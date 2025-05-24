# utils/logger.py

import datetime

def log_agent_prompt(agent: str, prompt: str, response: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = f"logs/{agent}_{datetime.datetime.now().date()}.log"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}] {agent} Prompt:\n{prompt}\n\nResponse:\n{response}\n" + "-"*60 + "\n")
