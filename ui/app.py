import streamlit as st
import sys
import os

# Add root path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.simulation_engine import run_simulation
from memory.response_log import get_all_logs

# ---------------------- Streamlit UI ----------------------

st.set_page_config(page_title="CivicMind - AI Policy Simulator", layout="centered")

st.title("🧠 CivicMind")
st.subheader("AI-Powered Local Governance Simulator")

st.markdown("Choose a public policy and simulate how different stakeholders react.")

# Sample policy options
sample_policies = [
    "A ₹100 congestion tax will be implemented in the city center on weekdays.",
    "Plastic bags will be completely banned in all city markets from next month.",
    "Public parks will close at 5 PM for safety, monitored by surveillance drones.",
    "City will increase property tax by 15% to fund green infrastructure."
]

# Policy input
policy = st.selectbox("📜 Choose a policy to simulate:", sample_policies)

st.markdown("### 🎭 Customize Agent Personas (optional)")

citizen_persona = st.selectbox("Citizen Persona", ["low-income commuter", "elderly resident", "college student"])
citizen_tone = st.selectbox("Citizen Tone", ["frustrated", "hopeful", "neutral"])

business_persona = st.selectbox("Business Persona", ["small shop owner", "restaurant manager", "logistics operator"])
business_tone = st.selectbox("Business Tone", ["concerned", "opportunistic", "neutral"])

politician_tone = st.selectbox("Politician Tone", ["formal", "optimistic", "technical"])
activist_tone = st.selectbox("Activist Tone", ["angry", "passionate", "rational"])


if st.button("Run Simulation 🚀"):
    with st.spinner("Simulating A2A civic debate..."):
        result = run_simulation(
            policy,
            citizen_persona,
            citizen_tone,
            business_persona,
            business_tone,
            politician_tone,
            activist_tone
        )

    st.success("Debate complete! See what each stakeholder said:")

    # Show Round 1 responses
    st.markdown("### Round 1 Responses")
    st.markdown("#### 🧑‍💼 PoliticianBot")
    st.info(result["politician_round1"])

    st.markdown("#### 👤 CitizenBot")
    st.info(result["citizen_round1"])
    st.info(f"**Sentiment Score:** {result['citizen_sentiment_1']}")

    st.markdown("#### 🏪 BusinessBot")
    st.info(result["business_round1"])
    st.info(f"**Sentiment Score:** {result['business_sentiment_1']}")

    st.markdown("#### 🧕 ActivistBot")
    st.info(result["activist_round1"])
    st.info(f"**Sentiment Score:** {result['activist_sentiment_1']}")

    st.markdown("---")

    # Show Round 2 responses
    st.markdown("### Round 2 Responses")
    st.markdown("#### 🧑‍💼 PoliticianBot")
    st.info(result["politician_round2"])

    st.markdown("#### 👤 CitizenBot")
    st.info(result["citizen_round2"])
    st.info(f"**Sentiment Score:** {result['citizen_sentiment_2']}")

    st.markdown("#### 🏪 BusinessBot")
    st.info(result["business_round2"])
    st.info(f"**Sentiment Score:** {result['business_sentiment_2']}")

    st.markdown("#### 🧕 ActivistBot")
    st.info(result["activist_round2"])
    st.info(f"**Sentiment Score:** {result['activist_sentiment_2']}")

    st.markdown("---")

    # Journalist summary
    st.markdown("### 📰 JournalistBot Summary")
    st.success(result["journalist_summary"])

    # Optional: download summary
    st.download_button("📥 Download Summary", result["journalist_summary"], file_name="civicmind_summary.txt")

    st.markdown("### ⚖️ JudgeBot Evaluation")
    st.code(result["judge_report"])

    # st.markdown("---")
    # st.markdown("### 🕓 Debate Timeline")

    # timeline = get_all_logs()
    # if timeline:
    #     for entry in timeline:
    #         st.markdown(f"**🗣️ {entry['agent']}**")
    #         st.markdown(entry["text"])
    #         st.markdown("---")
    # else:
    #     st.info("No debate timeline found.")



else:
    st.warning("Choose a policy and click 'Run Simulation 🚀' to begin.")
