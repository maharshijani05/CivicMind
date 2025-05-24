# agents/business.py

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_business_response(policy: str, persona: str = "small shop owner") -> str:
    """
    Returns a response from BusinessBot for the given policy.
    """
    prompt = f"""
You are a business owner named Priya who runs a shop in the city center.
You are a {persona} trying to survive in a competitive economy.

A new government policy has been proposed: "{policy}".

Describe how this policy could impact your business operations, customers, costs, and profitability.
Respond from a practical and emotional point of view.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
