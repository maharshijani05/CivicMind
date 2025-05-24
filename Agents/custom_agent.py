from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_custom_agent_response(policy: str, prior_context: list, persona: str, tone: str) -> str:
    """
    Generate a response for the custom agent.

    Args:
        policy (str): The policy text being discussed.
        prior_context (list): List of strings with previous conversation turns.
        persona (str): The custom agent's persona description.
        tone (str): The tone/style the custom agent should use.

    Returns:
        str: The generated response by the custom agent.
    """
    
    # Combine prior context into a single string with line breaks
    context_text = "\n".join(prior_context)

    # Create the prompt for the LLM
    prompt = (
        f"You are a civic debate agent with the persona: {persona}.\n"
        f"The tone of your response should be: {tone}.\n\n"
        f"Current policy being discussed:\n{policy}\n\n"
        f"Previous conversation:\n{context_text}\n\n"
        f"Please respond thoughtfully, reflecting your persona and tone."
    )

    # Call your LLM's chat/completion API here (pseudo-code)
    response = llm.chat.completions.create(
        model="llama3-70b-8192", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    # Extract the text reply from the LLM response
    agent_reply = response.choices[0].message.content.strip()

    return agent_reply
