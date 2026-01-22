# agents/journalist.py

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_journalist_summary(policy: str, citizen: str, business: str, politician: str, activist: str,custom_agent=None) -> str:
    """
    Returns a news-style article summarizing the multi-agent debate on a given policy.
    """
    prompt = f"""
You are an unbiased journalist reporting on a public town hall where a new policy was discussed.

Policy: "{policy}"

Here are the highlights from different stakeholders:

- Citizen: {citizen}
- Business Owner: {business}
- Politician: {politician}
- Activist: {activist}
- Custom Agent: {custom_agent if custom_agent else "No custom agent response provided."}

Write a professional and engaging news article that summarizes the different perspectives. Include a short headline, opening paragraph, and a balanced overview of reactions from each agent. Keep it neutral but insightful.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.65
    )

    return response.choices[0].message.content.strip()
