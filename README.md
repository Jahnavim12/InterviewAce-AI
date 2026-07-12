# InterviewAce AI – AI-Powered Interview Trainer Agent using IBM watsonx.ai

**Problem Statement No. 22:** Interview Trainer Agent

InterviewAce AI is a professional, deployment-ready interactive web application designed to help job seekers train for technical and behavioral interviews. Powered by **IBM watsonx.ai** and the **IBM Granite LLM model**, the platform generates tailored, context-aware interview questions matching specific job roles and experience levels, grades candidates' answers objectively on a 0-10 scale, and provides granular, actionable feedback.

---

## 🚀 Key Features

*   **Custom Selection**: Choose from 5 primary industry roles (Software Engineer, Data Scientist, Product Manager, QA Engineer, UX Designer) and 4 experience levels (Fresher, Junior, Mid-Level, Senior).
*   **Context-Aware Question Generation**: Generates high-quality technical or behavioral questions dynamically. History tracking ensures candidates do not receive duplicate questions in the same session.
*   **Objective AI Evaluation**: Candidate explanations are evaluated using Granite's analytical capabilities, scoring them from 0.0 to 10.0.
*   **Granular Performance Review**: Explicit breakdown highlighting the candidate's **Strengths** (conceptual clarity, core keywords) and **Weaknesses / Areas of Improvement**.
*   **Suggested Model Answers**: Every evaluated question provides a comprehensive, structured template answer for study and improvement.
*   **API Connection Indicator & Sandbox Fallback**: Visual dashboard indicator displaying active IBM watsonx.ai connections, with a robust local mock sandbox engine to test the app fully offline or without API keys.
*   **Automated Slide Deck Generator**: Built-in script that automatically generates a professional 10-slide PowerPoint presentation (`InterviewAce_AI_Presentation.pptx`) for academic or corporate submissions.

---

## 🛠️ Technology Stack

*   **Frontend**: Python + Streamlit (Curated slate-indigo premium dark theme layout)
*   **AI Engine**: IBM watsonx.ai (ModelInference client)
*   **Foundation LLM**: IBM Granite (`ibm/granite-3-0-8b-instruct`)
*   **Configuration**: python-dotenv (Secure key and project environment loading)
*   **Widescreen Presentation Builder**: python-pptx (Automated 16:9 PowerPoint compiler)
*   **Deployment Hosting**: Streamlit Community Cloud (Supports live deployment)

---

## 📊 System Architecture & Flow

```
User (Input Role/Exp) ──> Streamlit UI ──> Session State Manager
                                              │
  ┌───────────────────────────────────────────┘
  ▼
Prompt Builder (Interpolate parameters)
  │
  ▼
IBM watsonx.ai Client (ModelInference API Call)
  │
  ▼
Granite Foundation Model (ibm/granite-3-0-8b-instruct)
  │
  ├─> Generation Flow: Formulates a customized interview question
  └─> Evaluation Flow: Renders Score (0-10) + Strengths/Weaknesses + Suggested Answer
  │
  ▼
Streamlit UI Output Parser (Render JSON as beautiful Cards & Badges)
```

---

## 🔧 Installation and Configuration

### Prerequisites
*   Python 3.9 or higher

### Step 1: Clone or Download the Project
Ensure all files are placed in your working folder:
```bash
InterviewAce-AI/
│
├── app.py              # Main Streamlit interface
├── ibm_watson.py       # Watsonx.ai integration and mock fallback wrapper
├── prompts.py          # Prompt templates for question and evaluation
├── requirements.txt    # Project dependencies
├── generate_ppt.py     # Automated presentation compiler
└── .env                # Environment keys (to be created)
```

### Step 2: Install Dependencies
Open your terminal inside the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 3: Configure IBM Watsonx.ai Credentials (Optional but Recommended)
1. Log in to your [IBM Cloud Lite](https://cloud.ibm.com) account.
2. Create a **watsonx.ai** service instance.
3. Generate an **API Key** from the IBM Cloud dashboard (Manage > Access (IAM) > API Keys).
4. Create a **watsonx.ai project** and copy the **Project ID** from the project's *Manage* tab.
5. Identify your regional endpoint URL (e.g. `https://us-south.ml.cloud.ibm.com`).
6. Copy `.env.example` to a new file named `.env` and enter your credentials:
```env
WATSONX_APIKEY=your_actual_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_actual_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-0-8b-instruct
```
*Note: If no `.env` file is present, the app will launch in Sandbox Mode automatically, allowing you to test all features using a local knowledge library.*

---

## 🏃 Running the Application

### 1. Launch the Interview Interface
Start the Streamlit application using your terminal:
```bash
streamlit run app.py
```
This opens the interface in your browser (usually at `http://localhost:8501`).

### 2. Generate the PowerPoint Presentation (10 Slides)
Compile your internship submission PowerPoint deck by running the utility script:
```bash
python generate_ppt.py
```
This creates `InterviewAce_AI_Presentation.pptx` in your folder. The slides cover:
1. Title Page
2. Problem Statement
3. Existing System & Limitations
4. Proposed Solution
5. System Architecture
6. Application Workflow
7. Technology Stack
8. UI/UX Design Highlights
9. Future Scope
10. Conclusion & Social Impact

---

## 🎯 Evaluation Criteria Mapping

Our implementation directly satisfies the internship evaluation parameters:

*   **IBM Cloud Platform**: Integrates directly with IBM watsonx.ai and the open-source enterprise Granite model using the official `ibm-watsonx-ai` SDK.
*   **Scalability & Innovativeness**: Leverages serverless API integration with structured state tracking. The prompt templates force highly structured JSON outputs from Granite, ensuring predictable parsing.
*   **Social & Beneficial Impact**: Offers free, premium, context-specific interview feedback for underprivileged candidates, students, and job seekers without access to expensive private coaching.
*   **Readiness for Deployment**: Pre-configured configuration templates and an automated backend fallback mechanism make it immediately compatible with Streamlit Community Cloud hosting.
*   **Market Viability**: Solves a critical bottleneck in the recruitment lifecycle for both candidates (training) and talent acquisition platforms (automated screening pre-assessments).
*   **Future Scope**: Includes defined roadmap extensions for resume-upload parsing, voice audio analysis, and company-specific mocking.
