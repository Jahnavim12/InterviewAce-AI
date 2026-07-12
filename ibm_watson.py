import os
import json
import re
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WatsonxClient:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_APIKEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL")
        self.model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-0-8b-instruct")
        
        # Check if we should run in mock mode
        if not self.api_key or not self.project_id or not self.url or "your_ibm_cloud_api_key" in self.api_key:
            self.is_mock = True
            self.model = None
        else:
            try:
                from ibm_watsonx_ai import Credentials
                from ibm_watsonx_ai.foundation_models import ModelInference
                
                credentials = Credentials(
                    url=self.url,
                    api_key=self.api_key
                )
                
                # Setup inference parameters
                params = {
                    "decoding_method": "greedy",
                    "max_new_tokens": 800,
                    "min_new_tokens": 1,
                    "temperature": 0.0
                }
                
                self.model = ModelInference(
                    model_id=self.model_id,
                    credentials=credentials,
                    project_id=self.project_id,
                    params=params
                )
                self.is_mock = False
            except Exception as e:
                print(f"Error initializing Watsonx Client: {e}. Falling back to Mock Mode.")
                self.is_mock = True
                self.model = None

        # Mock question library for fallback
        self.mock_questions = {
            "Software Engineer": {
                "Fresher": [
                    "Explain the difference between abstract classes and interfaces in Object-Oriented Programming.",
                    "What is a binary search tree (BST), and what is its average-case search time complexity?",
                    "What is the difference between process and thread? Explain with an example.",
                    "Explain the concept of method overloading vs method overriding in Java/C++."
                ],
                "Junior": [
                    "Describe the MVC (Model-View-Controller) architecture and how data flows between components.",
                    "What are database indexes, and how do they speed up query execution? Are there any downsides?",
                    "Explain the differences between REST and GraphQL APIs. When would you use which?",
                    "How do you handle exceptions in Python/JavaScript? What is the purpose of the 'finally' block?"
                ],
                "Mid-Level": [
                    "Explain how you would handle race conditions in a multithreaded database-backed application.",
                    "Describe the difference between SQL and NoSQL databases. When would you choose NoSQL over SQL?",
                    "How do you design a secure user authentication system? What key algorithms and practices do you use?",
                    "Explain the concept of connection pooling in databases and why it is important."
                ],
                "Senior": [
                    "How would you design a distributed rate limiter for an API supporting millions of requests per day?",
                    "Discuss the architectural trade-offs of microservices vs monoliths, specifically focusing on data consistency.",
                    "Explain how you would scale a web application to handle a sudden 10x traffic spike.",
                    "Describe your approach to code reviews and technical debt management in a growing team."
                ]
            },
            "Data Scientist": {
                "Fresher": [
                    "What is overfitting in machine learning, and how can you prevent or mitigate it?",
                    "Explain the difference between supervised and unsupervised learning with examples.",
                    "What is the Central Limit Theorem, and why is it important in statistics?",
                    "Describe the difference between L1 (Lasso) and L2 (Ridge) regularization."
                ],
                "Junior": [
                    "Explain how a Random Forest classifier works. How does it differ from a single Decision Tree?",
                    "What are precision, recall, and F1-score? When would you prioritize precision over recall?",
                    "Explain the steps you would take to handle missing data in a dataset before training a model.",
                    "What is cross-validation, and why is it preferred over a simple train-test split?"
                ],
                "Mid-Level": [
                    "Explain the concept of Gradient Boosting. How do XGBoost and LightGBM optimize this process?",
                    "How would you handle highly imbalanced datasets in a classification problem (e.g., fraud detection)?",
                    "Explain the difference between PCA (Principal Component Analysis) and t-SNE. When is each used?",
                    "What are word embeddings? Explain the difference between Word2Vec and transformer-based embeddings."
                ],
                "Senior": [
                    "How would you design an end-to-end recommendation engine for an e-commerce platform with cold-start problems?",
                    "How do you monitor machine learning models in production for data drift and concept drift?",
                    "Explain the trade-offs between deploying a large deep learning model vs a simpler linear model in production.",
                    "Describe how you would design an A/B testing framework to evaluate a new model's performance on live users."
                ]
            },
            "Product Manager": {
                "Fresher": [
                    "What is a Minimum Viable Product (MVP), and why is it important in product development?",
                    "How do you define success for a new feature? Explain with metrics.",
                    "What is user-centered design, and how does it impact product decisions?",
                    "Explain the difference between Agile and Waterfall methodologies."
                ],
                "Junior": [
                    "How do you prioritize features for a product roadmap? Explain using a framework like RICE or MoSCoW.",
                    "How do you handle feature requests from key stakeholders that don't align with your product vision?",
                    "Describe how you would conduct user research to validate a new product concept.",
                    "What is a product requirement document (PRD), and what are its key components?"
                ],
                "Mid-Level": [
                    "How would you handle a situation where the engineering team estimates a critical feature will take twice as long as expected?",
                    "Describe how you would launch a product in a competitive market where there are established players.",
                    "How do you use quantitative user data vs qualitative feedback to iterate on a product?",
                    "Explain how you would measure and improve user retention for a subscription-based mobile app."
                ],
                "Senior": [
                    "Describe a time you had to pivot a product strategy based on user data and market conditions. What was the outcome?",
                    "How do you balance short-term revenue goals with long-term product vision and user trust?",
                    "How would you design a pricing strategy for a new B2B enterprise SaaS product?",
                    "How do you alignment product strategies across cross-functional teams (Engineering, Sales, Marketing, Design)?"
                ]
            },
            "QA Engineer": {
                "Fresher": [
                    "What is the difference between manual testing and automated testing?",
                    "Explain the bug lifecycle from discovery to verification and closure.",
                    "What is the difference between functional and non-functional testing?",
                    "What is boundary value analysis, and how do you apply it in test case design?"
                ],
                "Junior": [
                    "What is regression testing, and how do you determine which test cases to run after a code change?",
                    "Explain the difference between black box, white box, and grey box testing.",
                    "How do you write an effective bug report? What details are essential?",
                    "What is Page Object Model (POM) in Selenium automation, and why is it used?"
                ],
                "Mid-Level": [
                    "How do you design a test automation strategy for an API. What tools and assertions do you use?",
                    "Describe how you integrate automated tests into a CI/CD pipeline (e.g., Jenkins, GitHub Actions).",
                    "How do you handle flaky tests in an automated test suite?",
                    "What is load testing vs stress testing? What tools would you use to perform them?"
                ],
                "Senior": [
                    "How would you build a scalable test automation framework from scratch for a complex web/mobile platform?",
                    "How do you measure and report quality metrics (e.g., code coverage, defect density) to executive stakeholders?",
                    "How do you manage testing for a microservices architecture where services are deployed independently?",
                    "Describe how you would transition a legacy manual QA team into an automated SDET organization."
                ]
            },
            "UX Designer": {
                "Fresher": [
                    "What are the core principles of User-Centered Design (UCD)?",
                    "What is the difference between a wireframe, a mockup, and a prototype?",
                    "Explain the concept of visual hierarchy and how you establish it in a layout.",
                    "What is the role of typography and color theory in user interface design?"
                ],
                "Junior": [
                    "How do you conduct usability testing, and how do you translate qualitative feedback into design revisions?",
                    "What is an empathy map, and how does it help in the UX research phase?",
                    "Describe the difference between responsive design and adaptive design.",
                    "How do you ensure your designs meet accessibility guidelines (e.g., WCAG 2.1 AA)?"
                ],
                "Mid-Level": [
                    "How do you design a complex dashboard interface for data-heavy applications, balancing density and readability?",
                    "Describe how you construct and maintain a Design System. What are the key benefits?",
                    "How do you handle disagreements with engineering about a design's technical feasibility?",
                    "Explain your process for mapping out user journeys and flow diagrams for a new application flow."
                ],
                "Senior": [
                    "How do you measure the ROI (Return on Investment) of UX design interventions in a business?",
                    "How do you design for complex user workflows that span across multiple platforms (mobile, web, physical)?",
                    "Describe how you lead design workshops (like Design Sprints) with diverse stakeholders to solve problems.",
                    "How do you balance aesthetic design desires with conversion rate optimization (CRO) goals?"
                ]
            }
        }

    def generate_question(self, role, experience, history=[]):
        """
        Generates an interview question for a given role and experience level.
        Takes history (list of previous questions) into account to avoid duplicates.
        """
        if self.is_mock:
            # Fallback to local questions
            questions = self.mock_questions.get(role, {}).get(experience, ["Explain standard concepts related to your role."])
            # Filter out questions already in history
            available = [q for q in questions if q not in history]
            if not available:
                available = questions
            return random.choice(available)
        
        # Live IBM Watsonx API
        from prompts import QUESTION_GEN_PROMPT
        prompt = QUESTION_GEN_PROMPT.format(role=role, experience=experience)
        
        # Add context of previous questions if history exists
        if history:
            history_text = "\n- ".join(history)
            prompt = f"{prompt}\n\nAvoid generating the following questions that were already asked:\n- {history_text}\n\nQuestion:"
            
        try:
            response = self.model.generate(prompt=prompt)
            result = response['results'][0]['generated_text'].strip()
            # Clean up the output in case LLM wraps it in quotes or prefixes
            result = result.strip('"').strip("'").strip()
            # If the response is empty, fallback to mock
            if not result:
                return self.generate_question(role, experience, history)
            return result
        except Exception as e:
            print(f"Error calling Watsonx API: {e}. Falling back to Mock.")
            # Auto fallback to mock for this request
            self.is_mock = True
            question = self.generate_question(role, experience, history)
            self.is_mock = False # restore state
            return question

    def evaluate_answer(self, question, user_answer, role, experience):
        """
        Evaluates the user's answer and returns a dictionary with:
        score (float), strengths (list), weaknesses (list), suggested_answer (str).
        """
        if not user_answer.strip():
            return {
                "score": 0.0,
                "strengths": ["None provided."],
                "weaknesses": ["The answer was left blank. You must provide an answer to be evaluated."],
                "suggested_answer": "Please write a response to receive a suggested answer guide."
            }

        if self.is_mock:
            return self._mock_evaluate(question, user_answer)

        # Live IBM Watsonx API
        from prompts import EVALUATION_PROMPT
        prompt = EVALUATION_PROMPT.format(
            role=role,
            experience=experience,
            question=question,
            user_answer=user_answer
        )
        
        try:
            response = self.model.generate(prompt=prompt)
            raw_text = response['results'][0]['generated_text'].strip()
            return self._parse_json_response(raw_text)
        except Exception as e:
            print(f"Error calling Watsonx Evaluation API: {e}. Falling back to Mock.")
            return self._mock_evaluate(question, user_answer)

    def _parse_json_response(self, text):
        """
        Robustly extracts and parses JSON from model output.
        """
        try:
            # Try parsing directly
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to search for json block
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            
            # Fallback parsing or mock if formatting completely failed
            print(f"Could not parse JSON. Raw output: {text}")
            return {
                "score": 6.5,
                "strengths": ["Answer contains relevant keywords and concepts."],
                "weaknesses": ["Response formatting error occurred during AI evaluation. Structure could be improved."],
                "suggested_answer": "Review core concepts matching this topic in technical documentations."
            }

    def _mock_evaluate(self, question, user_answer):
        """
        Simulates a detailed AI evaluation locally.
        Uses simple keyword counts and word counts to calculate a score and feedback.
        """
        word_count = len(user_answer.split())
        
        # Define some general positive/negative keywords for heuristics
        positive_keywords = ["because", "example", "architecture", "design", "manage", "database", "scale", "optimize", 
                             "interface", "process", "thread", "override", "overload", "model", "view", "controller",
                             "prevent", "reduce", "test", "user", "workflow", "system", "index"]
        
        matches = [word for word in positive_keywords if word in user_answer.lower()]
        
        # Heuristic scoring
        if word_count < 10:
            score = round(random.uniform(2.0, 4.0), 1)
            strengths = ["Attempted to answer the question."]
            weaknesses = [
                "The answer is extremely brief. Try to explain in detail.",
                "Missing definitions, technical context, and examples."
            ]
        elif word_count < 30:
            score = round(random.uniform(4.5, 6.5), 1)
            strengths = ["Identified the core concept."] if len(matches) > 1 else ["Provided a basic response."]
            weaknesses = [
                "Explain how it works, rather than just what it is.",
                "Include a code block, diagram description, or practical example."
            ]
        else:
            score = round(min(6.5 + (len(matches) * 0.4) + (word_count * 0.005), 9.8), 1)
            strengths = [
                "Good length and vocabulary in explanation.",
                "Demonstrated understanding of core concepts with proper keywords."
            ]
            weaknesses = [
                "Could detail the trade-offs or alternate approaches.",
                "Try incorporating a real-world scenario where you applied this."
            ]
            if len(matches) > 4:
                strengths.append("Structured the answer logical and clearly.")

        # Pick a suggested answer based on question or general outline
        suggested_answer = (
            "A perfect answer should cover:\n"
            "1. **Direct Definition**: Give a clear, one-sentence definition of the concept.\n"
            "2. **Core Mechanisms**: Explain how it works step-by-step (e.g., syntax, layout, logic flow).\n"
            "3. **Practical Example**: Illustrate with a concrete code snippet or real-world project example.\n"
            "4. **Trade-offs / Key Differences**: Mention when to use it, limits, or comparisons to alternatives.\n\n"
            f"Here is an outline matching your question: \"{question}\"\n"
            "• State the key term clearly (e.g., OOP, MVC, BST search times).\n"
            "• Highlight the operational benefits (e.g., reusability, cleaner code, O(log n) efficiency).\n"
            "• Discuss limitations (e.g., index write overheads, microservice serialization costs).\n"
            "• Emphasize your personal experience or a practical case study."
        )

        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggested_answer": suggested_answer
        }
