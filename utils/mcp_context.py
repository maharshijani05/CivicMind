# utils/mcp_context.py

def build_agent_prompt(
    role: str,
    policy: str,
    prior_context: list[str],
    persona: str = "",
    tone: str = "realistic",
    reply_to_agent: str = "",
    reply_to_text: str = ""
) -> str:
    """
    Constructs a structured prompt for an agent using MCP-style context.
    Optionally enables replying directly to a previous agent's message.
    """

    # Join prior messages into context block
    joined_context = "\n".join(prior_context) if prior_context else ""

    # Add targeted counter-response if applicable
    if reply_to_agent and reply_to_text:
        quote_reply_block = f"""
🔁 Respond directly to the following statement made by {reply_to_agent}:
"{reply_to_text}"

Do not ignore this. Disagree or agree explicitly and elaborate.
"""
    else:
        quote_reply_block = ""

    # Final prompt construction
    prompt = f"""
You are acting as a {role} in a simulated civic policy debate.

🧠 Policy:
"{policy}"

🧑 Your Persona:
{persona}

🎤 Tone of Voice:
Speak in a {tone}, context-aware, and authentic way.

🧩 What Others Have Said:
{joined_context}

{quote_reply_block}

✍️ Now share your thoughts on this policy. Consider how it impacts you, your values, and your goals.
Respond in a short, natural paragraph as if you're speaking at a public hearing.
"""
    return prompt.strip()
