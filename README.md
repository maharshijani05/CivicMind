# 🧠 CivicMind

**CivicMind** is an AI-powered civic policy simulation platform where intelligent agents debate, analyze, and evaluate policies from various stakeholder perspectives like citizens, politicians, activists, businesses, and more. It uses LLMs to emulate real-world civic discourse and generates structured feedback, feasibility assessments, and sentiment evaluations for proposed policies.

---

## 🌟 Features

* 🤖 **AI Persona Agents**: Simulated stakeholders (Politician, Citizen, Activist, Business, Journalist, Custom) provide diverse viewpoints.
* 🔁 **Multi-Round Debates**: Agents refine their opinions across simulation rounds.
* 📈 **Sentiment Analysis**: Tracks how agents emotionally perceive the policy.
* 🧑‍⚖️ **JudgeBot Evaluation**: Produces structured reports including feasibility, conflict zones, social impact, and final recommendation.
* 📊 **Interactive Dashboard**: Streamlit-based UI to run simulations and visualize sentiment trends.
* 📄 **PDF Summary Generator**: Exports JudgeBot reports and simulation logs.

---

## 🏗️ Project Structure

```
CivicMind/
├── agents/
│   ├── activist.py
│   ├── business.py
│   ├── citizen.py
│   ├── custom_agent.py
│   ├── judge.py
│   ├── journalist.py
│   └── politician.py
│
├── memory/
│   ├── memory_module.py
│   └── response_log.py
│
├── ui/
│   ├── app.py                 # Main Streamlit app (entry point)
│   └── simulation_engine.py   # Orchestrates multi-agent interactions
│
├── utils/
│   ├── agents_responded.py
│   ├── logger.py
│   ├── mcp_context.py
│   ├── pdf_generator.py
│   ├── prompts.py
│   ├── sentiment.py
│   └── summarizer.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/maharshijani05/CivicMind.git
cd CivicMind
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Launch the App

```bash
streamlit run ui/app.py
```

---

## 🧪 Tech Stack

* **Python 3.11**
* **LangChain** + **Groq (LLM API)**
* **Streamlit** (for UI)
* **Matplotlib / Pandas** (for sentiment visualization)

---

## 🤖 Agents

Each agent is designed with a unique persona and tone:

* **PoliticianBot**: Represents governmental perspectives.
* **CitizenBot**: Voices concerns of the general populace.
* **BusinessBot**: Focuses on economic and business implications.
* **ActivistBot**: Advocates for social and environmental issues.
* **CustomBot**: User-defined agent to introduce additional viewpoints.

---

## 🧠 JudgeBot Evaluation

After the debate, JudgeBot provides a comprehensive evaluation that includes:

1. **Policy Summary**: A concise overview of the discussed policy.
2. **Stakeholder Sentiment Scores**: Sentiment ratings for each agent.
3. **Feasibility Score**: Assessment of the policy's practicality.
4. **Predicted Social Impact**: Analysis of potential societal effects.
5. **Potential Conflicts**: Identification of areas of disagreement.
6. **Recommendation**: Suggests whether to accept, revise, or reject the policy.

---

## 📊 Visualizations

The application includes visual representations of sentiment trends across debate rounds, helping users to:

* Track changes in agent sentiments.
* Identify consensus or divergence among stakeholders.
* Understand the dynamics of the debate.

---

## 📚 Example Use Case

1. Paste a policy proposal.
2. Select which agents to include (Citizen, Business, etc).
3. Run simulation (2 rounds of A2A discussion).
4. JudgeBot generates evaluation.
5. Visualize sentiment trends.
6. Export PDF report.

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

Developed by [Maharshi Jani](https://github.com/maharshijani05) as part of an initiative to enhance civic engagement through AI-driven simulations.
