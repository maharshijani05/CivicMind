# utils/mcp_context.py

def build_agent_prompt(role: str, policy: str, prior_context: list[str], persona: str = "", tone: str = "realistic") -> str:
    """
    Constructs a structured prompt for an agent using MCP-style context.
    """
    joined_context = "\n".join(prior_context) if prior_context else ""

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

✍️ Now share your thoughts on this policy. Consider how it impacts you, your values, and your goals.
Respond in a short, natural paragraph as if you're speaking at a public hearing.
"""
    return prompt.strip()
