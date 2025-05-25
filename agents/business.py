# agents/business.py

from groq import Groq
from dotenv import load_dotenv
import os
from utils.mcp_context import build_agent_prompt

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_business_response(policy: str, prior_context=[], persona="small shop owner", tone="concerned",reply_to_agent= "",reply_to_text= "") -> str:
    """
    Returns a response from BusinessBot using MCP-style context.
    """
    prompt = build_agent_prompt(
        role="business owner",
        policy=policy,
        prior_context=prior_context,
        persona=persona,
        tone=tone,
        reply_to_agent=reply_to_agent,
        reply_to_text=reply_to_text
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
