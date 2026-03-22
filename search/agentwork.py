from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def explain_code(user_question: str, context: dict) -> dict:
    prompt_context = context.get("prompt_context", "No code context available.")
    prompt = f"""You are an expert code analysis assistant.
Below is the relevant code extracted from the repository, organized into sections:
primary code: the function or class directly relevant to the user's question
dependencies: other functions called by the primary code
called by: functions that use the primary code

{prompt_context}

---
User question: {user_question}

Instructions:
1. Quote the specific function or class that directly answers the question.
2. Explain it clearly. If parameters are involved, use the dependencies section.
3. If a full class was retrieved, explain each method and how they work together.
4. Keep it concise and developer-friendly.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {
        "question": user_question,
        "intent": context.get("intent"),
        "code_context": prompt_context,
        "explanation": response.text,
    }