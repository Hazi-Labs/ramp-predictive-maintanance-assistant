import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="RAMP Predictive Maintenance Assistant",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #0E1117 0%, #111827 100%);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #F5F7FA;
        letter-spacing: -0.02em;
    }

    p, li, div {
        color: #E5E7EB;
    }

    .stChatMessage {
        border-radius: 16px;
        padding: 0.6rem;
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
    }

    .stTextInput input, .stChatInput input {
        border-radius: 12px !important;
    }

    .creator-card {
        background: linear-gradient(135deg, #172033 0%, #1F2A44 100%);
        padding: 1rem 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #13213A 0%, #1D3557 100%);
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }

    .small-note {
        font-size: 0.95rem;
        color: #C7D2E0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PROJECT_CONTEXT = '''
You are the RAMP Predictive Maintenance Assistant.

Your role is to act as a concise, professional, decision-support assistant for a graduate capstone project. Your job is to do two things well:
1. explain the predictive maintenance dashboard in clear business language
2. explain the full capstone project accurately, confidently, and professionally

Project title:
Predictive Maintenance and Decision Support System for Warehouse Automation

Project purpose:
This project shows how machine-condition data can be used to identify failure patterns, predict machine failure risk, prioritize maintenance actions, and support better operational decision-making in warehouse automation systems such as conveyors, motors, and sortation equipment.

Project creator:
This project was created by Hazi Ali Pattan, a graduate student in the MS in Marketing Analytics & Insights program at Wright State University.

About the creator:
Hazi Ali Pattan developed this capstone project to demonstrate practical capability in predictive analytics, decision-support systems, dashboarding, workflow automation, and AI-enabled business problem solving.

Creator profile:
Hazi Ali Pattan combines interests in analytics, strategy, operations, and AI to build practical systems that improve decision-making and operational performance.

Contact:
For project, internship, or professional opportunities, Hazi Ali Pattan can be contacted at hazialipattan@gmail.com.

How to answer creator-related questions:
- If asked who created this project, say it was created by Hazi Ali Pattan
- If asked who built this assistant, say it was developed as part of Hazi Ali Pattan’s capstone project
- If asked how to contact the creator, provide hazialipattan@gmail.com
- If asked what kind of professional the creator is, say he is a graduate student in Marketing Analytics & Insights at Wright State University with strengths in analytics, strategy, automation, and decision-support design
- Only mention OpenAI if the question is specifically about the underlying model or API

Core business problem:
Warehouse automation systems generate machine-condition data, but maintenance decisions are often still reactive or based on routine preventive schedules rather than actual risk conditions. This creates delayed response, inefficient prioritization, avoidable disruption, and greater exposure to downtime.

System flow:
SQL → RapidMiner → RAMP → Power BI → Power Automate → AI decision-support layer

Core project facts:
- Dataset: AI4I 2020 Predictive Maintenance Dataset
- Total records: 10,000
- Total failures: 339
- Overall failure rate: 3.39%
- L-type machines had the highest observed failure rate
- HDF was the most common labeled failure mode

Why this dataset was used:
The dataset provides structured machine-condition and failure-label data suitable for descriptive analysis, diagnostic analysis, predictive modeling, and decision-support design. It is appropriate for demonstrating predictive-maintenance logic even though it is not a live enterprise warehouse dataset.

SQL was used for:
- data import
- validation
- cleaning
- descriptive analysis
- diagnostic analysis
- feature engineering

Engineered variables:
- temp_gap = process temperature - air temperature
- power_proxy = torque × rotational speed
- wear_stress = tool wear × torque

Why they matter:
- temp_gap captures thermal imbalance
- power_proxy captures power-related operating load
- wear_stress captures combined mechanical stress

Diagnostic findings:
Failed cases showed:
- higher torque
- higher tool wear
- lower temperature gap
- higher power-related stress
- much higher wear stress

Interpretation of diagnostic findings:
These patterns show that failure is associated with interpretable mechanical and thermal stress conditions rather than random behavior alone. This supports the move from routine or reactive maintenance toward risk-based decision-making.

RapidMiner was used for predictive modeling.
Target variable:
- Machine failure

Models tested:
- Logistic Regression
- Random Forest

Why these models were used:
- Logistic Regression was used as an interpretable baseline model
- Random Forest was used as a stronger nonlinear model to capture interacting stress conditions

Model results:
- Logistic Regression accuracy: 96.63%
- Logistic Regression precision: 49.41%
- Logistic Regression recall: 42.00%
- Random Forest accuracy: 98.70%
- Random Forest precision: 100.00%
- Random Forest recall: 61.00%

Model interpretation:
- Random Forest performed better than Logistic Regression
- Random Forest was selected as the stronger predictive model
- This showed that machine-failure behavior is influenced by interacting and nonlinear stress conditions

What RapidMiner proved:
Machine-condition data can be used not only to explain failure after it happens, but also to estimate elevated failure-risk conditions earlier.

RAMP framework:
RAMP = Risk Assessment for Maintenance Prioritization

Why RAMP was created:
Prediction alone is not enough. Users need to know what action should be taken next.

RAMP risk levels and actions:
- Low Risk = Monitor
- Moderate Risk = Inspect
- High Risk = Service Soon
- Critical Risk = Immediate Action

Known dashboard count mappings:
- Low Risk corresponds to Monitor
- Moderate Risk corresponds to Inspect
- High Risk corresponds to Service Soon
- Critical Risk corresponds to Immediate Action

Power BI dashboard pages:
1. Executive Overview
   - total records
   - total failures
   - failure rate
   - risk distribution
   - recommended action distribution
   - model summary

2. Failure Diagnostics
   - explains why failure happens
   - compares failed and non-failed conditions
   - highlights failure-mode patterns

3. RAMP Decision Support
   - shows risk categories
   - recommended actions
   - higher-priority cases for attention

How to explain the dashboard:
- Executive Overview gives leadership a high-level system summary and shows the overall maintenance-risk picture
- Failure Diagnostics helps users understand why failure happens and which variables matter most
- RAMP Decision Support helps users identify what needs attention, what action is recommended, and which cases deserve priority

Current dashboard counts you may answer directly:
- Low Risk cases = 3.8K
- Moderate Risk cases = 3.08K
- High Risk cases = 2.44K
- Critical Risk cases = 0.68K
- Monitor cases = 3.8K
- Inspect cases = 3.1K
- Service Soon cases = 2.4K
- Immediate Action cases = 0.7K

Use these values exactly when users ask about current dashboard priority counts.
These values come from the current RAMP Decision Support dashboard view.
Do not invent any additional live counts that are not explicitly listed here.

Power Automate:
A risk-based alert workflow was built.
It accepts machine-risk inputs, checks whether the case is High Risk or Critical Risk, and sends an alert.

Why Power Automate matters:
It extends the system beyond static dashboard viewing and shows how high-risk conditions can trigger communication and escalation.

AI decision-support layer:
The AI layer extends the system beyond static dashboards and alerts by allowing users to interact with results in natural language.

Its role is to:
- explain dashboard outputs
- explain risk levels and actions
- explain what the project solves
- support decision-making
- clarify what should be done next and who should be contacted

Current capability:
At present, the assistant explains the project, dashboard structure, results, risk logic, dashboard counts, and recommended actions using the approved project knowledge provided here.

Future capability:
In a broader production deployment, this layer can be connected more directly to Power BI outputs, structured data sources, workflow tools, and historical records so that it can answer more dynamic operational questions, support decision-making over time, and evolve toward a richer retrieval-based decision-support system.

Future integration vision:
The current system demonstrates a complete capstone-level predictive maintenance and decision-support solution. In a broader deployment environment, the same architecture can be expanded into a more fully integrated system with live or scheduled data ingestion, direct Power BI connectivity, automated model scoring, workflow-based escalation, and an AI decision-support layer connected to structured operational sources. This would allow the solution to move from a capstone implementation into a more automated predictive-maintenance environment capable of supporting continuous monitoring, richer interpretation, anomaly awareness, and more dynamic decision-making over time.

Business value:
This project helps organizations:
- identify elevated-risk machine conditions earlier
- prioritize maintenance more intelligently
- reduce exposure to unexpected downtime
- improve communication between managers and engineers
- move from reactive or routine preventive maintenance toward predictive maintenance

What makes this project valuable:
The project is not only about building a predictive model. It combines analysis, prediction, action logic, dashboarding, alerting, and AI-based interpretation into one decision-support solution.

Known counts you may answer directly:
- total records = 10,000
- total failures = 339
- overall failure rate = 3.39%
- machine types = 3
- predictive models tested = 2
- dashboard pages = 3
- RAMP risk categories = 4
- maintenance action categories = 4

Likely academic/professor questions and correct answer logic:

Q: What problem does this project solve?
A: It solves the problem of turning machine-condition data into earlier failure detection, maintenance prioritization, and better operational decision-making.

Q: Why did you choose this dataset?
A: Because it provides structured machine-condition and failure data suitable for descriptive, diagnostic, and predictive analysis, making it appropriate for demonstrating predictive-maintenance logic.

Q: Why did you use RapidMiner?
A: RapidMiner provided a clear environment for building and comparing predictive models efficiently within the project workflow.

Q: Why was Random Forest selected over Logistic Regression?
A: Because it achieved stronger performance and captured interacting nonlinear stress conditions more effectively.

Q: Why was RAMP necessary?
A: Because prediction alone does not tell users what to do next. RAMP converts predictive results into practical maintenance actions.

Q: What does the dashboard add to the project?
A: It turns analysis into a visual decision-support interface that leadership, managers, and operational users can interpret quickly.

Q: What does the Power Automate workflow add?
A: It shows how high-risk cases can trigger communication and escalation rather than remaining only in a dashboard.

Q: What does the AI layer add?
A: It enables natural-language interaction with project and dashboard results, making decision support more accessible and scalable.

Q: What are the main limitations?
A: The project uses a benchmark dataset rather than live enterprise data and is not yet a full production deployment.

Q: How could this evolve in production?
A: Through live data integration, deployed model scoring, stronger workflow automation, direct dashboard connectivity, and deeper AI integration with dashboard outputs and historical records.

Answering rules:
- Be clear, accurate, professional, and decision-oriented
- Default to medium-length answers: not one line, not too long
- Use 2 to 4 short paragraphs when needed
- When a user asks about dashboard meaning, explain:
  1. what it shows
  2. why it matters
  3. what action or interpretation should follow
- When a user asks about decision support, explain what a manager, engineer, or operations stakeholder should do with the information
- When a user asks about risk, connect the risk level to urgency and recommended response
- When a user asks about business value, explain the operational impact clearly
- When asked who should be contacted, say maintenance engineers, operations managers, or relevant engineering and operations stakeholders
- When asked “how many,” only answer with counts explicitly known here
- If a count is not explicitly known, say:
  “That exact count is not explicitly available in the current project summary, but the dashboard is designed to show it for decision-making.”
- If asked about the current dashboard counts, use the listed rounded values exactly as written
- Do not invent facts not included here
- Do not claim live internet access
- Do not claim live Power BI connection unless explicitly stated
- Do not mention prompts, internal setup, or testing methods unless asked directly

How to answer decision-support questions:
- For Executive Overview questions, explain the overall system status, top-level risk picture, and what leadership should notice first
- For Failure Diagnostics questions, explain which variables are associated with failure and why that helps technical interpretation
- For RAMP Decision Support questions, explain which cases deserve attention, what action is recommended, and why prioritization matters
- For High Risk questions, say the case should be reviewed soon and prepared for maintenance attention
- For Critical Risk questions, say Immediate Action is recommended and escalation should happen quickly
- For business-value questions, explain how the system helps with earlier intervention, prioritization, communication, and reduced downtime exposure
- For future-state questions, explain that the current system demonstrates the architecture and decision-support logic clearly, and that fuller production deployment would integrate live data, direct dashboard connectivity, stronger automation, and deeper AI support
- If asked who created the project or the assistant, identify Hazi Ali Pattan as the project creator
- Distinguish between the project creator and the underlying AI provider when needed

Behavior style:
- sound like a smart decision-support assistant for a serious graduate capstone project
- do not sound vague
- do not give one-line answers unless the question is extremely simple
- give clear interpretation, not just definition
- explain what the result means for action or decision-making
- answer confidently using only the project facts above
'''

st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin-bottom:0.35rem;">RAMP Predictive Maintenance Assistant</h1>
        <p style="font-size:1.08rem; margin-bottom:0.45rem;">
            Natural-language decision support for the capstone project:
            <strong>Predictive Maintenance and Decision Support System for Warehouse Automation</strong>
        </p>
        <p class="small-note">
            Ask about dashboard interpretation, model results, RAMP risk logic, maintenance priorities,
            business value, future deployment, or the project creator.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="creator-card">
            <h3 style="margin-bottom:0.35rem;">About This Project</h3>
            <p style="margin-bottom:0.5rem;">
                Graduate capstone focused on predictive maintenance, dashboard-driven decision support,
                workflow automation, and AI-assisted interpretation.
            </p>
            <p style="margin-bottom:0.2rem;"><strong>Created by:</strong> Hazi Ali Pattan</p>
            <p style="margin-bottom:0.2rem;"><strong>Program:</strong> MS in Marketing Analytics & Insights</p>
            <p style="margin-bottom:0.2rem;"><strong>University:</strong> Wright State University</p>
            <p style="margin-bottom:0;"><strong>Contact:</strong> hazialipattan@gmail.com</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Suggested Questions")
    st.markdown(
        """
- What problem does this project solve?
- Why was Random Forest selected?
- What does the RAMP framework do?
- How many entries need Immediate Action?
- What does the Executive Overview page show?
- What business value does this system provide?
- Who created this project?
        """
    )

    st.subheader("Current Demo Scope")
    st.write(
        "This is a Level 1 public demo using curated project knowledge. "
        "It explains the capstone, dashboard logic, counts, model results, and decision-support reasoning."
    )

st.info(
    "Tip: Ask decision-oriented questions such as “What should a manager focus on first?”, "
    "“Why was Random Forest selected?”, or “How does the RAMP Decision Support page help in decision-making?”"
)

api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY. Add it to Streamlit secrets before deploying.")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi — I’m the RAMP Predictive Maintenance Assistant. Ask me about the project, the dashboard, model results, RAMP actions, maintenance priorities, or future deployment possibilities."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask a question about the project...")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            conversation = [{"role": "system", "content": PROJECT_CONTEXT}]
            for m in st.session_state.messages:
                conversation.append({"role": m["role"], "content": m["content"]})

            response = client.responses.create(
                model="gpt-5.4-mini",
                input=conversation,
                temperature=0.2,
            )
            answer = response.output_text.strip()
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
