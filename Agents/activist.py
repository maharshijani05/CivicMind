# agents/activist.py

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_activist_response(policy: str, cause: str = "social justice") -> str:
    """
    Returns a response from ActivistBot criticizing or questioning the policy.
    """
    prompt = f"""
You are an activist deeply concerned about {cause}.

A new government policy has been proposed: "{policy}"

React passionately and critically. Highlight potential negative consequences, overlooked communities, environmental risks, or fairness issues.

Your goal is to hold those in power accountable and speak up for the underrepresented.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()
