# utils/sentiment.py

from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_sentiment_score_new(policy: str, persona: str, tone: str, response_text: str) -> int:
    """
    Uses Groq LLM to evaluate sentiment score (1-5) of an agent's response,
    taking into account the persona and their likely emotional stance on the policy.
    """

    prompt = f"""
You are a sentiment evaluation assistant designed to assess how a stakeholder with a specific persona
feels emotionally about a civic policy, based on their response.

Here is the context:

---
**Policy**:
{policy}

**Persona**: {persona}
**Tone**: {tone}

**Response Text**:
\"\"\"{response_text}\"\"\"
---

As this persona, consider how positively or negatively they feel about this policy based on their core beliefs,
tone, and the contents of their response. Assign a sentiment score on this scale:

- 1 = Very Negative
- 2 = Slightly Negative
- 3 = Neutral
- 4 = Slightly Positive
- 5 = Very Positive

Respond in the following JSON format only:
{{
  "score": <integer from 1 to 5>
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        raw_content = response.choices[0].message.content.strip()
        sentiment_data = json.loads(raw_content)
        return sentiment_data.get("score", 3)
    except Exception as e:
        print(f"[Sentiment Scoring Error] {e}")
        return 3
