# agents/judge.py

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_judge_evaluation(policy: str, citizen: str, business: str, politician: str, activist: str) -> str:
    """
    JudgeBot provides a neutral, structured evaluation of the overall policy debate.
    """

    prompt = f"""
You are a neutral civic AI judge. Four stakeholders just debated a policy.

Policy: "{policy}"

Citizen said: {citizen}
Business said: {business}
Politician said: {politician}
Activist said: {activist}

Evaluate the overall tone, fairness, and potential success of this policy.

Output a structured summary with:
- Equity Score (0–10)
- Public Acceptance (0–10)
- Economic Impact (0–10)
- Overall Verdict
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content.strip()
