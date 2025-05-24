import streamlit as st
import sys
import pandas as pd
import os

# Add root path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.simulation_engine import run_simulation
from memory.response_log import get_all_logs
from utils.pdf_generator import generate_judge_pdf


# ---------------------- Streamlit UI ----------------------

st.set_page_config(page_title="CivicMind - AI Policy Simulator", layout="centered")

st.title("🧠 CivicMind")
st.subheader("AI-Powered Local Governance Simulator")

st.markdown("Choose a public policy and simulate how different stakeholders react.")

# Sample policy options
sample_policies = [
    "City will subsidize solar panel installations for residential buildings.",
    "Public transport fares will be reduced by 25% during peak hours.",
    "Weekly community town halls will be held to gather citizen feedback.",
    "Garbage collection will now occur only once a week to cut costs.",
    "A ₹200 toll will be imposed on all private vehicles entering the city center."
]

citizen_persona_options = [
    "low-income commuter",
    "elderly resident",
    "college student",
    "daily wage worker",
    "environment-conscious youth"
]

citizen_tone_options = [
    "frustrated",
    "hopeful",
    "neutral",
    "grateful",
    "outraged"
]

business_persona_options = [
    "small shop owner",
    "restaurant manager",
    "tech startup founder",
    "logistics operator",
    "mall administrator"
]

business_tone_options = [
    "concerned",
    "opportunistic",
    "neutral",
    "resistant",
    "optimistic"
]

politician_tone_options = [
    "formal",
    "optimistic",
    "technical",
    "defensive",
    "visionary"
]

activist_tone_options = [
    "angry",
    "passionate",
    "rational",
    "hopeful",
    "sarcastic"
]


# Policy input
policy = st.selectbox("📜 Choose a policy to simulate:", sample_policies)

st.markdown("### 🎭 Customize Agent Personas")
customize_tones = st.toggle("Customize Agent Tones Manually?", value=True)

col1, col2 = st.columns(2)
with col1:
    citizen_persona = st.selectbox("👤 Citizen Persona",citizen_persona_options)
with col2:
    business_persona = st.selectbox("🏪 Business Persona",business_persona_options)
    
if customize_tones:
    col3, col4 = st.columns(2)
    with col3:
        citizen_tone = st.selectbox("🎭 Citizen Tone",citizen_tone_options)
    with col4:
        business_tone = st.selectbox("📈 Business Tone",business_tone_options)

    # Politician tone + Activist tone
    col5, col6 = st.columns(2)
    with col5:
        politician_tone = st.selectbox("🧑‍💼 Politician Tone",politician_tone_options)
    with col6:
        activist_tone = st.selectbox("🧕 Activist Tone",activist_tone_options)
else:
    citizen_tone = None
    business_tone = None
    politician_tone = None
    activist_tone = None

with st.expander("➕ Add Custom Civic Agent"):
    custom_agent_name = st.text_input("Agent Name (e.g., 'NGO', 'Legal Expert')").strip().lower()
    custom_agent_persona = st.text_area("Agent Persona", placeholder="Who is this agent and what do they represent?")
    custom_agent_tone = st.selectbox("Communication Tone", ["neutral", "aggressive", "optimistic", "pessimistic", "inquisitive"])

    add_custom_agent = st.button("Add Custom Agent")

if add_custom_agent:
    if custom_agent_name and custom_agent_persona:
        st.session_state['custom_agent'] = {
            "name": custom_agent_name,
            "persona": custom_agent_persona,
            "tone": custom_agent_tone
        }
        st.success(f"✅ Custom agent '{custom_agent_name.capitalize()}' added!")
    else:
        st.error("Please fill in both name and persona.")

custom_agent = st.session_state.get('custom_agent', None)


if st.button("Run Simulation 🚀"):
    with st.spinner("Simulating A2A civic debate..."):
        result = run_simulation(
            policy,
            citizen_persona,
            citizen_tone,
            business_persona,
            business_tone,
            politician_tone,
            activist_tone,
            tone_mode="manual" if customize_tones else "auto",
            custom_agent=custom_agent
        )
    
    logs = result["tone_logs"]
    
    df_logs = pd.DataFrame(logs)
    df_logs = df_logs.sort_values(by=["round", "agent"])

    st.success("Debate complete! See what each stakeholder said:")

    # Show Round 1 responses
    st.markdown("### Round 1 Responses")
    st.markdown("#### 🧑‍💼 PoliticianBot")
    st.info(result["politician_round1"])

    st.markdown("#### 👤 CitizenBot")
    st.info(result["citizen_round1"])
    # st.info(f"**Sentiment Score:** {result['citizen_sentiment_1']}")

    st.markdown("#### 🏪 BusinessBot")
    st.info(result["business_round1"])
    # st.info(f"**Sentiment Score:** {result['business_sentiment_1']}")

    if custom_agent:
        st.markdown(f"#### 🤖 {custom_agent['name'].capitalize()}")
        st.info(result.get("custom_agent_round1", "No response available"))

    st.markdown("#### 🧕 ActivistBot")
    st.info(result["activist_round1"])
    # st.info(f"**Sentiment Score:** {result['activist_sentiment_1']}")

    st.markdown("---")

    # Show Round 2 responses
    st.markdown("### Round 2 Responses")
    st.markdown("#### 🧑‍💼 PoliticianBot")
    st.info(result["politician_round2"])

    st.markdown("#### 👤 CitizenBot")
    st.info(result["citizen_round2"])
    # st.info(f"**Sentiment Score:** {result['citizen_sentiment_2']}")

    st.markdown("#### 🏪 BusinessBot")
    st.info(result["business_round2"])
    # st.info(f"**Sentiment Score:** {result['business_sentiment_2']}")
    if custom_agent:
        st.markdown(f"#### 🤖 {custom_agent['name'].capitalize()}")
        st.info(result.get("custom_agent_round2", "No response available"))

    st.markdown("#### 🧕 ActivistBot")
    st.info(result["activist_round2"])
    # st.info(f"**Sentiment Score:** {result['activist_sentiment_2']}")

    st.markdown("---")

    # Journalist summary
    st.markdown("### 📰 JournalistBot Summary")
    st.success(result["journalist_summary"])

    # Optional: download summary
    st.download_button("📥 Download Summary", result["journalist_summary"], file_name="civicmind_summary.txt")

    st.subheader("🎭 Agent Tones by Round")
    tone_table = df_logs.pivot_table(index="round", columns="agent", values="tone",aggfunc='first')
    st.dataframe(tone_table, use_container_width=True)


    st.markdown("### ⚖️ JudgeBot Evaluation")
    st.code(result["judge_report"])
    pdf_bytes = generate_judge_pdf(result["judge_report"])
    st.download_button(
        label="📄 Download Judge Report (PDF)",
        data=pdf_bytes,
        file_name="judge_report.pdf",
        mime="application/pdf"
    )

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
