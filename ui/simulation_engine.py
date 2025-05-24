# ui/simulation_engine.py

from agents.citizen import get_citizen_response
from agents.business import get_business_response
from agents.politician import get_politician_response
from agents.activist import get_activist_response
from agents.journalist import get_journalist_summary
from agents.judge import get_judge_evaluation

def run_simulation(
    policy: str,
    citizen_persona: str,
    citizen_tone: str,
    business_persona: str,
    business_tone: str,
    politician_tone: str,
    activist_tone: str
) -> dict:
    """
    Runs the CivicMind simulation with full A2A chaining and MCP input.
    """
    prior_context = []
    # Round 1: Politician proposes
    politician_response_1 = get_politician_response(policy=policy,prior_context=prior_context,persona="mayor of the city", tone=politician_tone)

    # Round 1: Citizen reacts to politician
    prior_context = [f"PoliticianBot: {politician_response_1}"]
    citizen_response_1 = get_citizen_response(
        policy=policy,
        prior_context=prior_context,
        persona=citizen_persona,
        tone=citizen_tone
    )

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

      # --- Round 2: Back to Politician to respond to others ---
    prior_context_round2 = [
        f"PoliticianBot: {politician_response_1}",
        f"CitizenBot: {citizen_response_1}",
        f"BusinessBot: {business_response_1}",
        f"ActivistBot: {activist_response_1}"
    ]

    politician_response_2 = get_politician_response(
        policy=policy,
        prior_context=prior_context_round2,
        persona="mayor of the city",
        tone=politician_tone
    )

    # Citizen responds again
    prior_context_round2.append(f"PoliticianBot: {politician_response_2}")
    citizen_response_2 = get_citizen_response(
        policy=policy,
        prior_context=prior_context_round2,
        persona=citizen_persona,
        tone=citizen_tone
    )

    # Business responds again
    prior_context_round2.append(f"CitizenBot: {citizen_response_2}")
    business_response_2 = get_business_response(
        policy=policy,
        prior_context=prior_context_round2,
        persona=business_persona,
        tone=business_tone
    )

    # Activist responds again
    prior_context_round2.append(f"BusinessBot: {business_response_2}")
    activist_response_2 = get_activist_response(
        policy=policy,
        prior_context=prior_context_round2,
        tone=activist_tone
    )

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
        activist=f"{activist_response_1}\n{activist_response_2}"
    )

    judge_report = get_judge_evaluation(
        policy=policy,
        citizen=f"{citizen_response_1}\n{citizen_response_2}",
        business=f"{business_response_1}\n{business_response_2}",
        politician=f"{politician_response_1}\n{politician_response_2}",
        activist=f"{activist_response_1}\n{activist_response_2}"
    )

    return {
        "policy": policy,
        "politician_round1": politician_response_1,
        "citizen_round1": citizen_response_1,
        "business_round1": business_response_1,
        "activist_round1": activist_response_1,
        "politician_round2": politician_response_2,
        "citizen_round2": citizen_response_2,
        "business_round2": business_response_2,
        "activist_round2": activist_response_2,
        "journalist_summary": journalist_summary,
        "judge_report": judge_report
    }
