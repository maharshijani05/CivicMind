# agents/judge.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_judge_evaluation(policy, citizen, business, politician, activist,custom_agent=None) -> str:
    """
    Returns a detailed evaluation report from JudgeBot including structured metrics, feasibility,
    stakeholder sentiments, and recommendations.
    """
    prompt = f"""
You are JudgeBot, an AI civic policy evaluator. Analyze the following policy debate.

Policy: {policy}

Stakeholder Responses:
- PoliticianBot: {politician}
- CitizenBot: {citizen}
- BusinessBot: {business}
- ActivistBot: {activist}
- Custom Agent: {custom_agent if custom_agent else "No custom agent response provided."}

Now provide a structured evaluation with the following format:

1. **Policy Summary**: Concise summary of the policy.
2. **Stakeholder Sentiment Scores (1-5)**:
   - Politician:
   - Citizen:
   - Business:
   - Activist:
   - Custom Agent Name(if applicable):
3. **Feasibility Score (1-5)**: How realistically this policy can be implemented and based on the sentiment scores.
4. **Predicted Social Impact**: Discuss positive and negative outcomes on the society.
5. **Potential Conflicts**: Identify key areas of disagreement or tension.
6. **Judge Recommendation**: Accept, Revise, or Reject, with reasoning.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
