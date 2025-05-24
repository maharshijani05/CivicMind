# ui/simulation_engine.py

from agents.citizen import get_citizen_response
from agents.business import get_business_response
from agents.politician import get_politician_response
from agents.activist import get_activist_response
from agents.journalist import get_journalist_summary
from agents.judge import get_judge_evaluation
from memory.memory_module import AgentMemory
from memory.response_log import log_response
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from agents.tone_selector import generate_initial_tones
from agents.tone_selector import generate_updated_tones
from agents.custom_agent import get_custom_agent_response


analyzer = SentimentIntensityAnalyzer()

memory = AgentMemory()
logs = []

def get_sentiment_score(text: str) -> float:
    vs = analyzer.polarity_scores(text)
    compound = vs["compound"]
    # Convert -1 to 1 scale into 1 to 5 scale
    score_1_to_5 = ((compound + 1) / 2) * 4 + 1
    return round(score_1_to_5, 2)  # Round to 2 decimal places for neatness

def run_simulation(
    policy: str,
    citizen_persona: str,
    citizen_tone: str,
    business_persona: str,
    business_tone: str,
    politician_tone: str,
    activist_tone: str,
    tone_mode: str = "manual",
    custom_agent: dict = None
) -> dict:

    if tone_mode == "auto":
        auto_tones = generate_initial_tones(policy)
        citizen_tone = auto_tones.get("citizen", "neutral")
        business_tone = auto_tones.get("business", "neutral")
        politician_tone = auto_tones.get("politician", "technical")
        activist_tone = auto_tones.get("activist", "rational")

    """
    Runs the CivicMind simulation with full A2A chaining and MCP input.
    """
    prior_context = []
    # Round 1: Politician proposes
    politician_response_1 = get_politician_response(policy=policy,prior_context=prior_context,persona="mayor of the city", tone=politician_tone)
    memory.add_to_memory("PoliticianBot", politician_response_1)
    log_response("PoliticianBot", politician_response_1)
    logs.append({
    "round": 1,
    "agent": "politician",
    "tone": politician_tone,
    "response": politician_response_1
    })


    # Round 1: Citizen reacts to politician
    prior_context = [f"PoliticianBot: {politician_response_1}"]
    citizen_response_1 = get_citizen_response(
        policy=policy,
        prior_context=prior_context,
        persona=citizen_persona,
        tone=citizen_tone
    )
    memory.add_to_memory("CitizenBot", citizen_response_1)
    log_response("CitizenBot", citizen_response_1)
    citizen_sentiment_1 = get_sentiment_score(citizen_response_1)
    logs.append({
    "round": 1,
    "agent": "citizen",
    "tone": citizen_tone,
    "response": citizen_response_1
    })

    # Round 1: Business reacts to both
    prior_context = [
        f"PoliticianBot: {politician_response_1}",
        f"CitizenBot: {citizen_response_1}"
    ]
    business_response_1 = get_business_response(
        policy=policy,
        prior_context=prior_context,
        persona=business_persona,
        tone=business_tone
    )
    memory.add_to_memory("BusinessBot", business_response_1)
    log_response("BusinessBot", business_response_1)
    business_sentiment_1 = get_sentiment_score(business_response_1)
    logs.append({
    "round": 1,
    "agent": "business",
    "tone": business_tone,
    "response": business_response_1
    })

    if custom_agent:
        custom_agent_name = custom_agent["name"]
        custom_agent_persona = custom_agent["persona"]
        custom_agent_tone = custom_agent["tone"]

        custom_response_1 = get_custom_agent_response(
            policy=policy,
            prior_context=prior_context,
            persona=custom_agent_persona,
            tone=custom_agent_tone
        )
        memory.add_to_memory(f"{custom_agent_name.capitalize()}Bot", custom_response_1)
        log_response(f"{custom_agent_name.capitalize()}Bot", custom_response_1)
        custom_sentiment_1 = get_sentiment_score(custom_response_1)
        prior_context.append(f"{custom_agent_name.capitalize()}Bot: {custom_response_1}")
        logs.append({
        "round": 1,
        "agent": custom_agent_name.lower(),
        "tone": custom_agent_tone,
        "response": custom_response_1
        })


    # Round 1: Activist reacts to all
    prior_context = [
        f"PoliticianBot: {politician_response_1}",
        f"CitizenBot: {citizen_response_1}",
        f"BusinessBot: {business_response_1}"
    ]
    activist_response_1 = get_activist_response(
        policy=policy,
        prior_context=prior_context,
        tone=activist_tone
    )
    memory.add_to_memory("ActivistBot", activist_response_1)
    log_response("ActivistBot", activist_response_1)
    activist_sentiment_1 = get_sentiment_score(activist_response_1)
    logs.append({
    "round": 1,
    "agent": "activist",
    "tone": activist_tone,
    "response": activist_response_1
    })

      # --- Round 2: Back to Politician to respond to others ---
    prior_context_round2 = [
        f"PoliticianBot: {politician_response_1}",  
        f"CitizenBot: {citizen_response_1}",
        f"BusinessBot: {business_response_1}",
        f"ActivistBot: {activist_response_1}"
    ]

    prior_responses_dict = {
    "politician": politician_response_1,
    "citizen": citizen_response_1,
    "business": business_response_1,
    "activist": activist_response_1
    }

    if custom_agent:
        prior_responses_dict[custom_agent_name.lower()] = custom_response_1

    updated_tones = generate_updated_tones(policy, prior_responses_dict)

    # Update tone variables from updated_tones dict
    politician_tone = updated_tones.get("politician", politician_tone)
    citizen_tone = updated_tones.get("citizen", citizen_tone)
    business_tone = updated_tones.get("business", business_tone)
    activist_tone = updated_tones.get("activist", activist_tone)

    politician_response_2 = get_politician_response(
        policy=policy,
        prior_context=prior_context_round2,
        persona="mayor of the city",
        tone=politician_tone
    )
    memory.add_to_memory("PoliticianBot", politician_response_2)
    log_response("PoliticianBot", politician_response_2)
    logs.append({
    "round": 2,
    "agent": "politician",
    "tone": politician_tone,
    "response": politician_response_2
    })

    # Citizen responds again
    prior_context_round2.append(f"PoliticianBot: {politician_response_2}")
    citizen_response_2 = get_citizen_response(
        policy=policy,
        prior_context=prior_context_round2,
        persona=citizen_persona,
        tone=citizen_tone
    )
    memory.add_to_memory("CitizenBot", citizen_response_2)
    log_response("CitizenBot", citizen_response_2)
    citizen_sentiment_2 = get_sentiment_score(citizen_response_2)
    logs.append({
    "round": 2,
    "agent": "citizen",
    "tone": citizen_tone,
    "response": citizen_response_2
    })

    # Business responds again
    prior_context_round2.append(f"CitizenBot: {citizen_response_2}")
    business_response_2 = get_business_response(
        policy=policy,
        prior_context=prior_context_round2,
        persona=business_persona,
        tone=business_tone
    )
    memory.add_to_memory("BusinessBot", business_response_2)
    log_response("BusinessBot", business_response_2)
    business_sentiment_2 = get_sentiment_score(business_response_2)
    logs.append({
    "round": 2,
    "agent": "business",
    "tone": business_tone,
    "response": business_response_2
    })

    if custom_agent:
        custom_response_2 = get_custom_agent_response(
            policy=policy,
            prior_context=prior_context_round2,
            persona=custom_agent_persona,
            tone=updated_tones.get(custom_agent_name, custom_agent_tone)
        )
        memory.add_to_memory(f"{custom_agent_name.capitalize()}Bot", custom_response_2)
        log_response(f"{custom_agent_name.capitalize()}Bot", custom_response_2)
        prior_context_round2.append(f"{custom_agent_name.capitalize()}Bot: {custom_response_2}")
        custom_sentiment_2 = get_sentiment_score(custom_response_2)
        logs.append({
        "round": 2,
        "agent": custom_agent_name.lower(),
        "tone": custom_agent_tone,
        "response": custom_response_2
        })


    # Activist responds again
    prior_context_round2.append(f"BusinessBot: {business_response_2}")
    activist_response_2 = get_activist_response(
        policy=policy,
        prior_context=prior_context_round2,
        tone=activist_tone
    )
    memory.add_to_memory("ActivistBot", activist_response_2)
    log_response("ActivistBot", activist_response_2)
    activist_sentiment_2 = get_sentiment_score(activist_response_2)
    logs.append({
    "round": 2,
    "agent": "activist",
    "tone": activist_tone,
    "response": activist_response_2
    })

    # Summarize by Journalist and Judge using full conversation history
    full_conversation = prior_context_round2 + [
        f"ActivistBot: {activist_response_2}"
    ]

    # Journalist summarizes everything
    journalist_summary = get_journalist_summary(
        policy=policy,
        citizen=f"{citizen_response_1}\n{citizen_response_2}",
        business=f"{business_response_1}\n{business_response_2}",
        politician=f"{politician_response_1}\n{politician_response_2}",
        activist=f"{activist_response_1}\n{activist_response_2}",
        custom_agent=f"{custom_response_1}\n{custom_response_2}" if custom_agent else None
    )
    memory.add_to_memory("JournalistBot", journalist_summary)
    log_response("JournalistBot", journalist_summary)
    

    judge_report = get_judge_evaluation(
        policy=policy,
        citizen=f"{citizen_response_1}\n{citizen_response_2}",
        business=f"{business_response_1}\n{business_response_2}",
        politician=f"{politician_response_1}\n{politician_response_2}",
        activist=f"{activist_response_1}\n{activist_response_2}",
        custom_agent=f"{custom_response_1}\n{custom_response_2}" if custom_agent else None
    )
    memory.add_to_memory("JudgeBot", judge_report)
    log_response("JudgeBot", judge_report)

    return {
        "policy": policy,
        "politician_round1": politician_response_1,
        "citizen_round1": citizen_response_1,
        "business_round1": business_response_1,
        "custom_agent_round1": custom_response_1,
        "activist_round1": activist_response_1,
        "politician_round2": politician_response_2,
        "citizen_round2": citizen_response_2,
        "business_round2": business_response_2,
        "custom_agent_round2": custom_response_2,  
        "activist_round2": activist_response_2,
        "journalist_summary": journalist_summary,
        "judge_report": judge_report,
        "round_1": {
            "PoliticianBot": politician_response_1,
            "CitizenBot": citizen_response_1,
            "BusinessBot": business_response_1,
            "CustomBot": custom_response_1, 
            "ActivistBot": activist_response_1
        },
        "round_2": {
            "PoliticianBot": politician_response_2,
            "CitizenBot": citizen_response_2,
            "BusinessBot": business_response_2,
            "CustomBot": custom_response_2,
            "ActivistBot": activist_response_2
        },
        "tone_logs": logs
    }