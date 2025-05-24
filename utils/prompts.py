def policy_tone_selection_prompt(policy: str) -> str:
    return f"""
Given the policy below, select the most likely tone for each stakeholder from the following list:
["angry", "concerned", "frustrated", "neutral", "hopeful", "opportunistic", "passionate", "rational", "technical", "formal", "optimistic"]

Respond ONLY in JSON format as follows:
{{
    "citizen": "<tone>",
    "business": "<tone>",
    "politician": "<tone>",
    "activist": "<tone>"
}}

Policy: {policy}
"""
def policy_tone_selection_prompt_2(policy: str, prior_context: str) -> str:
    return f"""
Given the following public policy and stakeholder responses, decide the most likely tone each stakeholder would adopt in the next round of discussion. Choose one tone per stakeholder from: ["angry", "frustrated", "concerned", "hopeful", "optimistic", "opportunistic", "technical", "formal", "rational", "passionate", "neutral"]

Policy: "{policy}"

Stakeholder Responses:
{prior_context}

Respond ONLY in JSON format as follows:
{{
    "citizen": "<tone>",
    "business": "<tone>",
    "politician": "<tone>",
    "activist": "<tone>"
}}
"""
