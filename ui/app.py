import streamlit as st
import sys
import pandas as pd
import os
import importlib
import plotly.graph_objects as go
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

# Add root path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ui.simulation_engine as simulation
from memory.response_log import get_all_logs
from utils.pdf_generator import generate_judge_pdf


# ---------------------- Streamlit UI ----------------------

st.set_page_config(page_title="CivicMind - AI Policy Simulator", layout="centered")

st.title("🧠 CivicMind")
st.subheader("AI-Powered Local Governance Simulator")

st.markdown("### 🧭 Policy Explorer: Upload or Paste Policy")

policy_mode = st.radio("Choose input method:", ["Upload PDF/Text File", "Paste Policy Text"])

uploaded_policy_text = ""

if policy_mode == "Upload PDF/Text File":
    uploaded_file = st.file_uploader("Upload a policy file (PDF or TXT)", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            uploaded_policy_text = "\n".join([page.extract_text() for page in reader.pages])
        elif uploaded_file.type == "text/plain":
            uploaded_policy_text = uploaded_file.read().decode("utf-8")

elif policy_mode == "Paste Policy Text":
    uploaded_policy_text = st.text_area("Paste your policy text here", height=300)

if uploaded_policy_text:
    if st.button("🧠 Extract Summary"):
        with st.spinner("Summarizing policy..."):
            from utils.summarizer import summarize_policy
            summary = summarize_policy(uploaded_policy_text)
            st.session_state["custom_summary"] = summary
            st.success("Summary extracted!")


st.markdown("Choose a public policy and simulate how different stakeholders react.")

# Sample policy options
sample_policies = [
    "City will subsidize solar panel installations for residential buildings.",
    "Public transport fares will be reduced by 25% during peak hours.",
    "Weekly community town halls will be held to gather citizen feedback.",
    "Garbage collection will now occur only once a week to cut costs.",
    "A ₹200 toll will be imposed on all private vehicles entering the city center.",
    "All government schools will receive free AI-based personalized learning tools for students.",
    "Local farmers' markets will receive funding for digital payment adoption and cold storage facilities.",
    "City parks will be mapped and listed in a public directory with opening hours and amenities.",
    "Water supply hours will be restricted to mornings only due to maintenance budget cuts.",
    "Unemployed citizens must pay a monthly administrative fee to access job-seeking services."
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
# policy = st.selectbox("📜 Choose a policy to simulate:", sample_policies)
if "custom_summary" in st.session_state:
    st.markdown("#### 📄 Extracted Policy Summary")
    st.info(st.session_state["custom_summary"])
    policy = st.session_state["custom_summary"]

else:
    policy = st.selectbox(
        "📜 Choose a policy to simulate:",
        options=sample_policies,
        index=0  # Optional: sets the default selected index
    )

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
        importlib.reload(simulation)
        result = simulation.run_simulation(
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

    st.session_state["simulation_result"] = result
    
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

# Only render results if simulation was already run
    # if "simulation_result" in st.session_state:
    #     result = st.session_state["simulation_result"]
        
    #     # Show the result (rounds, charts, etc.)
    #     st.markdown("### 🧾 Journalist Summary")
    #     st.write(result["journalist_summary"])

    #     # Download button
    #     st.download_button(
    #         label="📥 Download Summary",
    #         data=result["journalist_summary"],
    #         file_name="civicmind_summary.txt",
    #         mime="text/plain"
    #     )

    logs = get_all_logs()
    def prepare_sentiment_data(logs):
        """
        Returns a list of dictionaries containing:
        - agent
        - round_num
        - sentiment
        """
        data = []

        for entry in logs:
            if "agent" in entry and "round_num" in entry and "sentiment" in entry:
                data.append({
                    "agent": entry["agent"],
                    "round_num": entry["round_num"],
                    "sentiment": entry["sentiment"]
                })

        return data

    # def print_sentiment_scores(logs):
    #     agents = ["PoliticianBot", "CitizenBot", "BusinessBot", "ActivistBot", "CustomBot"]
    #     rounds = [1, 2]

    #     st.markdown("### 🧠 Sentiment Scores (Per Agent Per Round)")
    #     for round_num in rounds:
    #         st.markdown(f"#### 🔁 Round {round_num}")
    #         for agent in agents:
    #             # Find the entry for this agent in this round
    #             matching_entries = [entry for entry in logs if entry["agent"] == agent and entry["round_num"] == round_num]
    #             if matching_entries:
    #                 sentiment = matching_entries[0]["sentiment"]  # take first or latest, as needed
    #                 st.write(f"**{agent}**: Sentiment Score = {sentiment}")
    #             else:
    #                 st.write(f"**{agent}**: No response in this round.")

    # # st.markdown("### 📊 Sentiment Trends Across Rounds")
    # print_sentiment_scores(logs)

    def plot_sentiment_scores(logs):
        """
        Plots sentiment scores for each agent across rounds.
        """
        # Step 1: Prepare data
        df = pd.DataFrame([
            {
                "Agent": entry["agent"].replace("Bot", ""),  # Clean up labels
                "Round": entry["round_num"],
                "Sentiment": entry["sentiment"]
            }
            for entry in logs
            if "agent" in entry and "round_num" in entry and "sentiment" in entry
            and entry["agent"] in ["PoliticianBot", "CitizenBot", "BusinessBot", "ActivistBot", "CustomBot"]
        ])

        if df.empty:
            st.warning("No sentiment data available to plot.")
            return
        df["Sentiment"] = pd.to_numeric(df["Sentiment"], errors='coerce')
        # Optional: sort agent names for consistency
        agent_order = ["Citizen", "Business", "Politician", "Activist", "Custom"]
        df["Agent"] = pd.Categorical(df["Agent"], categories=agent_order, ordered=True)

        # Step 2: Plot
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x="Round", y="Sentiment", hue="Agent", marker="o", palette="Set2")

        plt.ylim(0, 6)
        plt.xticks([1, 2])
        plt.title("Sentiment Trend Across Rounds")
        plt.ylabel("Sentiment Score (1-5)")
        plt.xlabel("Round")
        plt.grid(True)
        plt.legend(title="Agent", loc="best")

        # Step 3: Streamlit display
        st.pyplot(plt)

    st.markdown("### 📊 Sentiment Trends Across Rounds")
    plot_sentiment_scores(logs)

    # Journalist summary
    st.markdown("### 📰 JournalistBot Summary")
    st.success(result["journalist_summary"])
    # st.download_button(
    #         label="📥 Download Summary",
    #         data=result["journalist_summary"],
    #         file_name="civicmind_summary.txt",
    #         mime="text/plain"
    #     )

    # if "simulation_result" in st.session_state:
    #     journalist_summary = st.session_state["simulation_result"]["journalist_summary"]
    #     st.download_button("📥 Download Summary", journalist_summary, file_name="civicmind_summary.txt")

    # Optional: download summary
    # st.download_button("📥 Download Summary", result["journalist_summary"], file_name="civicmind_summary.txt")

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

    if "custom_agent" in st.session_state: 
        del st.session_state["custom_agent"]
    
    if "custom_summary" in st.session_state:
        del st.session_state["custom_summary"]
    
    if "simulation_result" in st.session_state:
        del st.session_state["simulation_result"]



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
