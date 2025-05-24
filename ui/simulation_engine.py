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

    # Round 1: Politician proposes
    politician_response = get_politician_response(policy)

    # Round 2: Citizen reacts to politician
    prior_context = [f"PoliticianBot: {politician_response}"]
    citizen_response = get_citizen_response(
        policy=policy,
        prior_context=prior_context,
        persona=citizen_persona,
        tone=citizen_tone
    )

    # Round 3: Business reacts to both
    prior_context = [
        f"PoliticianBot: {politician_response}",
        f"CitizenBot: {citizen_response}"
    ]
    business_response = get_business_response(
        policy,
        prior_context,
        persona=business_persona,
        tone=business_tone
    )

    # Round 4: Activist reacts to all
    prior_context = [
        f"PoliticianBot: {politician_response}",
        f"CitizenBot: {citizen_response}",
        f"BusinessBot: {business_response}"
    ]
    activist_response = get_activist_response(
        policy,
        prior_context,
        tone=activist_tone
    )

    # Journalist summarizes everything
    journalist_summary = get_journalist_summary(
        policy=policy,
        citizen=citizen_response,
        business=business_response,
        politician=politician_response,
        activist=activist_response
    )

    judge_report = get_judge_evaluation(policy, citizen_response, business_response, politician_response, activist_response)

    return {
        "policy": policy,
        "politician": politician_response,
        "citizen": citizen_response,
        "business": business_response,
        "activist": activist_response,
        "journalist": journalist_summary,
        "judge": judge_report
    }
