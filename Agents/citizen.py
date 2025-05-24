# agents/citizen.py

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_citizen_response(policy: str, persona: str = "low-income worker") -> str:
    """
    Returns a response from CitizenBot for the given policy and persona.
    """
    prompt = f"""
You are a citizen named Raj, a {persona} who lives in a crowded city.
A new government policy has been proposed: "{policy}".

Describe how this policy will affect your life.
Respond emotionally and personally, as a real citizen might in a town hall.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
