# agents/politician.py

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_politician_response(policy: str, role: str = "Mayor of the city") -> str:
    """
    Returns a response from PoliticianBot defending the proposed policy.
    """
    prompt = f"""
You are the {role}, speaking at a public town hall.

The proposed policy is: "{policy}"

Justify this policy to the public.
Explain the reasoning, benefits, and long-term goals.
Address potential concerns respectfully but assertively.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content.strip()
