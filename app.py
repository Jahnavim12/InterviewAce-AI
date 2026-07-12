import streamlit as st
import time
from ibm_watson import WatsonxClient

# Page configuration
st.set_page_config(
    page_title="InterviewAce AI - AI Interview Trainer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State variables
if "client" not in st.session_state:
    st.session_state.client = WatsonxClient()

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "scores" not in st.session_state:
    st.session_state.scores = []

if "active_role" not in st.session_state:
    st.session_state.active_role = "Software Engineer"

if "active_experience" not in st.session_state:
    st.session_state.active_experience = "Fresher"

# Custom Premium Styling
st.markdown("""
    <style>
        /* Import premium font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Apply fonts and background styles */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Card Panel design */
        .card-panel {
            background-color: #1e293b;
            border-radius: 16px;
            padding: 28px;
            border: 1px solid #334155;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
            margin-bottom: 24px;
        }
        
        /* Typography adjustments */
        .title-text {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem;
            margin-bottom: 5px;
            text-align: center;
        }
        
        .subtitle-text {
            color: #94a3b8;
            font-size: 1.2rem;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 300;
        }
        
        /* Status badge stylings */
        .badge-active {
            background-color: rgba(6, 95, 70, 0.3);
            color: #34d399;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            border: 1px solid #059669;
            display: inline-block;
            margin-top: 10px;
        }
        
        .badge-mock {
            background-color: rgba(124, 45, 18, 0.3);
            color: #fb923c;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            border: 1px solid #ea580c;
            display: inline-block;
            margin-top: 10px;
        }
        
        /* Result Score visual */
        .score-circle {
            background: radial-gradient(circle, #1e1b4b 0%, #0f172a 100%);
            width: 140px;
            height: 140px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            border: 3px solid #6366f1;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
        }
        
        .score-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #f8fafc;
        }
        
        .score-max {
            font-size: 1rem;
            color: #6366f1;
            margin-left: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to reset the interview session
def reset_interview():
    st.session_state.current_question = ""
    st.session_state.history = []
    st.session_state.evaluation = None
    st.session_state.scores = []
    st.session_state.client = WatsonxClient() # Refresh config

# Sidebar configuration
with st.sidebar:
    st.image("assets/logo.png", width=70)
    st.markdown("<h2 style='margin-top:0px;'>Interview Configuration</h2>", unsafe_allow_html=True)
    
    # Selection inputs
    role = st.selectbox(
        "Select Target Job Role:",
        ["Software Engineer", "Data Scientist", "Product Manager", "QA Engineer", "UX Designer"],
        index=["Software Engineer", "Data Scientist", "Product Manager", "QA Engineer", "UX Designer"].index(st.session_state.active_role)
    )
    
    experience = st.selectbox(
        "Select Experience Level:",
        ["Fresher", "Junior", "Mid-Level", "Senior"],
        index=["Fresher", "Junior", "Mid-Level", "Senior"].index(st.session_state.active_experience)
    )
    
    # Save selection changes to state
    if role != st.session_state.active_role or experience != st.session_state.active_experience:
        st.session_state.active_role = role
        st.session_state.active_experience = experience
        reset_interview()
        
    st.markdown("---")
    st.markdown("### IBM Cloud Status")
    
    # API indicators
    if st.session_state.client.is_mock:
        st.markdown('<div class="badge-mock">🔌 Sandbox Mode (Fallback)</div>', unsafe_allow_html=True)
        st.caption("Using built-in local question database and evaluation heuristic. Add credentials to `.env` file to unlock live IBM watsonx.ai.")
    else:
        st.markdown('<div class="badge-active">⚡ IBM watsonx.ai (Active)</div>', unsafe_allow_html=True)
        st.caption(f"Connected using Granite LLM model: `{st.session_state.client.model_id}`")
        
    st.markdown("---")
    # Action buttons
    if st.button("🔄 Reset Interview Session", use_container_width=True):
        reset_interview()
        st.success("Session reset completed!")
        time.sleep(0.5)
        st.rerun()

# Main Application Hub
st.markdown('<h1 class="title-text">InterviewAce AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">AI-Powered Interview Trainer Agent powered by IBM Granite LLM</p>', unsafe_allow_html=True)

# Grid Layout for Analytics
col_info, col_progress = st.columns([2, 1])

with col_info:
    st.markdown(f"**Target Role:** {st.session_state.active_role} | **Experience:** {st.session_state.active_experience}")

with col_progress:
    if st.session_state.scores:
        avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.markdown(f"<div style='text-align:right;'><b>Questions Answered:</b> {len(st.session_state.scores)} | <b>Avg Score:</b> {avg_score:.2f}/10</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:right; color:#64748b;'>No questions answered yet.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main container based on state
if not st.session_state.current_question:
    # Welcome Layout
    st.markdown("""
        <div class="card-panel">
            <h3 style="margin-top:0px; color:#a855f7;">Welcome to InterviewAce AI!</h3>
            <p>Prepare for your next technical interview with an agent trained using IBM's enterprise-grade Granite LLM. Here is how it works:</p>
            <ol>
                <li>Select your target job role and experience level in the sidebar.</li>
                <li>Click <b>"Start Interview Session"</b> to generate your first tailored question.</li>
                <li>Write down your explanation and receive a detailed evaluation including:</li>
                <ul>
                    <li>An objective <b>AI Performance Score (0-10)</b>.</li>
                    <li>Specific <b>Strengths</b> and <b>Weaknesses</b> of your response.</li>
                    <li>A complete, expert-curated <b>Suggested Answer</b>.</li>
                </ul>
                <li>Proceed to the next question to build your average score!</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Interview Session", type="primary", use_container_width=True):
        with st.spinner("IBM watsonx.ai is compiling your first question..."):
            new_question = st.session_state.client.generate_question(
                st.session_state.active_role, 
                st.session_state.active_experience
            )
            st.session_state.current_question = new_question
            st.rerun()

else:
    # Active Question screen
    st.markdown(f"""
        <div class="card-panel">
            <h4 style="margin-top:0px; color:#818cf8; font-weight:600;">Question #{len(st.session_state.history) + 1}</h4>
            <p style="font-size:1.35rem; font-weight:400; line-height:1.6; color:#f1f5f9;">"{st.session_state.current_question}"</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Text input area for response
    # We use session state to preserve user answer
    user_ans = st.text_area(
        "Your Answer Explanation:", 
        placeholder="Provide a detailed, technical explanation. Use examples, code structures, or process stages to back your claim...",
        height=200
    )
    
    # Submit evaluation
    btn_eval, btn_skip = st.columns([3, 1])
    
    with btn_eval:
        if st.button("🔍 Evaluate Answer", type="primary", use_container_width=True, disabled=st.session_state.evaluation is not None):
            if not user_ans.strip():
                st.warning("Please type a response before evaluating.")
            else:
                with st.spinner("Sending answer to IBM Granite Model for comprehensive assessment..."):
                    eval_result = st.session_state.client.evaluate_answer(
                        st.session_state.current_question,
                        user_ans,
                        st.session_state.active_role,
                        st.session_state.active_experience
                    )
                    st.session_state.evaluation = eval_result
                    # Save score to stats
                    try:
                        score_val = float(eval_result.get("score", 0.0))
                        st.session_state.scores.append(score_val)
                    except:
                        st.session_state.scores.append(6.0)
                    st.rerun()
                    
    with btn_skip:
        if st.button("⏭️ Skip Question", use_container_width=True):
            with st.spinner("Generating next question..."):
                st.session_state.history.append(st.session_state.current_question)
                new_q = st.session_state.client.generate_question(
                    st.session_state.active_role,
                    st.session_state.active_experience,
                    st.session_state.history
                )
                st.session_state.current_question = new_q
                st.session_state.evaluation = None
                st.rerun()

    # Render evaluation results if present
    if st.session_state.evaluation:
        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#a855f7; text-align:center;'>AI Evaluation Report</h3>", unsafe_allow_html=True)
        
        col_score, col_details = st.columns([1, 2])
        
        with col_score:
            score = st.session_state.evaluation.get("score", 0.0)
            st.markdown(f"""
                <div class="card-panel" style="text-align:center; height:100%;">
                    <h4 style="margin-top:0px; color:#94a3b8; font-size:1.1rem; text-transform:uppercase; letter-spacing:1px;">Evaluation Score</h4>
                    <div class="score-circle">
                        <span class="score-value">{score}</span>
                        <span class="score-max">/10</span>
                    </div>
                    <p style="margin-top:20px; font-size:0.95rem; color:#94a3b8;">Scored by IBM Granite Agent</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col_details:
            strengths = st.session_state.evaluation.get("strengths", ["No strengths highlighted."])
            weaknesses = st.session_state.evaluation.get("weaknesses", ["No weaknesses highlighted."])
            
            # Format bullets with colors
            strengths_html = "".join([f"<li>✅ {item}</li>" for item in strengths])
            weaknesses_html = "".join([f"<li>⚠️ {item}</li>" for item in weaknesses])
            
            st.markdown(f"""
                <div class="card-panel" style="height:100%;">
                    <h4 style="margin-top:0px; color:#22c55e; font-size:1.2rem;">Strengths</h4>
                    <ul style="list-style-type:none; padding-left:0; color:#e2e8f0; line-height:1.6;">
                        {strengths_html}
                    </ul>
                    <h4 style="margin-top:20px; color:#f43f5e; font-size:1.2rem;">Weaknesses / Areas of Improvement</h4>
                    <ul style="list-style-type:none; padding-left:0; color:#e2e8f0; line-height:1.6;">
                        {weaknesses_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        # Suggested answer section
        st.markdown(f"""
            <div class="card-panel">
                <h4 style="margin-top:0px; color:#38bdf8; font-size:1.2rem;">Suggested Model Answer</h4>
                <div style="background-color:#0f172a; padding:20px; border-radius:8px; border:1px solid #1e293b; color:#e2e8f0; line-height:1.6; white-space: pre-line;">
                    {st.session_state.evaluation.get("suggested_answer", "Suggested outline is not available.")}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Next question CTA
        if st.button("➡️ Proceed to Next Question", type="primary", use_container_width=True):
            with st.spinner("Retrieving next question..."):
                # Append current question to history
                st.session_state.history.append(st.session_state.current_question)
                # Generate new question
                new_q = st.session_state.client.generate_question(
                    st.session_state.active_role,
                    st.session_state.active_experience,
                    st.session_state.history
                )
                st.session_state.current_question = new_q
                st.session_state.evaluation = None
                st.rerun()

# Footer branding
st.markdown("<br><hr style='border-color: #334155;'><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b; font-size:0.9rem;'>InterviewAce AI | Powered by Streamlit & IBM watsonx.ai | Dedicated to Social & Professional Impact</p>", unsafe_allow_html=True)
