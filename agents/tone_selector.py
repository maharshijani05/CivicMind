from groq import Groq
import os
from utils.prompts import policy_tone_selection_prompt
from utils.prompts import policy_tone_selection_prompt_2
import json

# Initialize client correctly
llm = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Ensure you’ve set your key in .env or elsewhere

def generate_initial_tones(policy: str) -> dict:
    prompt = policy_tone_selection_prompt(policy)

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a tone selector that chooses emotional tones for 4 stakeholders based on a policy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    try:
        tones = json.loads(response.choices[0].message.content.strip())
        # print("🔍 Detected Initial Tones:", tones)
        return tones  # Or use json.loads() if your response is JSON
    except Exception as e:
        print("Tone parsing failed1:", e)
        return {
            "citizen": "neutral",
            "business": "neutral",
            "politician": "technical",
            "activist": "rational"
        }

def generate_updated_tones(policy: str, prior_responses: dict) -> dict:
    context = "\n".join([f"{agent.capitalize()} said: \"{resp}\"" for agent, resp in prior_responses.items()])
    prompt = policy_tone_selection_prompt_2(policy, context)

    try:
        response = llm.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",  # Ensure this is your working model
            temperature=0.7
        )
        # print("Raw LLM Response:\n", response.choices[0].message.content)
        tones = json.loads(response.choices[0].message.content.strip())
        return tones
    except Exception as e:
        print("Tone parsing failed2:", e)
        return {
            "citizen": "neutral",
            "business": "neutral",
            "politician": "neutral",
            "activist": "neutral"
        }