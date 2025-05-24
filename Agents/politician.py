# agents/politician.py

from groq import Groq
from dotenv import load_dotenv
import os
from utils.mcp_context import build_agent_prompt

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prior_context=[]
persona="mayor of the city"
tone="formal"

def get_politician_response(policy: str,prior_context=[], persona="mayor of the city", tone="formal") -> str:
    """
    Returns a response from PoliticianBot using MCP-style context.
    """
    prompt = build_agent_prompt(
        role="politician",
        policy=policy,
        prior_context=prior_context,
        persona=persona,
        tone=tone
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content.strip()
