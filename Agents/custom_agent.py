from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_custom_agent_response(
    policy: str,
    prior_context: list,
    persona: str,
    tone: str,
    reply_to_agent: str = "",
    reply_to_text: str = ""
) -> str:
    """
    Generate a response for the custom agent.

    Args:
        policy (str): The policy text being discussed.
        prior_context (list): List of strings with previous conversation turns.
        persona (str): The custom agent's persona description.
        tone (str): The tone/style the custom agent should use.
        reply_to_agent (str): Name of the agent this response is targeting.
        reply_to_text (str): The message being replied to.

    Returns:
        str: The generated response by the custom agent.
    """
    
    context_text = "\n".join(prior_context)

    # Optional quote + response block
    if reply_to_agent and reply_to_text:
        quote_block = (
            f"\n\nDirectly respond to the following statement from {reply_to_agent}:\n"
            f"\"{reply_to_text}\"\n"
            f"Explicitly agree or disagree, and explain your reasoning.\n"
        )
    else:
        quote_block = ""

    prompt = (
        f"You are a civic debate agent with the persona: {persona}.\n"
        f"The tone of your response should be: {tone}.\n\n"
        f"Current policy being discussed:\n{policy}\n\n"
        f"Previous conversation:\n{context_text}"
        f"{quote_block}\n\n"
        f"Please respond thoughtfully, reflecting your persona and tone."
    )

    response = llm.chat.completions.create(
        model="llama3-70b-8192", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
