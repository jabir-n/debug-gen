import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# UI Setup
st.set_page_config(page_title="Debugging Assistant")

st.title("🐞 AI Debugging Assistant")
st.write("Paste your error and code. Get real debugging insights.")

# Inputs
error = st.text_area("⚠️ Paste Error Message")
code = st.text_area("💻 Paste Your Code")

language = st.selectbox(
    "🧠 Select Programming Language",
    ["Python", "JavaScript", "C++", "Java", "Other"]
)

simple_mode = st.checkbox("Explain in simple terms (Beginner Mode)")

# Core Debug Function
def debug_agent(error, code, language, simple_mode):

    explanation_style = (
        "Explain like teaching a beginner in very simple terms."
        if simple_mode
        else "Explain in a detailed and technical manner."
    )

    prompt = f"""
    You are a senior software engineer and expert debugger.

    Analyze the issue carefully.

    Programming Language: {language}

    Error:
    {error}

    Code:
    {code}

    Instructions:
    {explanation_style}

    Provide output in this structured format:

    1. Root Cause
    - What exactly is wrong

    2. Severity
    - Beginner mistake / Syntax error / Logic error / Architecture issue

    3. Fix
    - Steps to fix the issue

    4. Explanation
    - Why this happened

    5. Corrected Code
    - Provide full fixed version of the code

    6. Prevention Tips
    - How to avoid this in future
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an elite debugging expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


# Run Debugger
if st.button("🚀 Debug Now"):

    if not error or not code:
        st.warning("⚠️ Please provide both error and code.")
    else:
        with st.spinner("Analyzing the problem..."):

            try:
                result = debug_agent(error, code, language, simple_mode)

                st.subheader("🧠 Debug Analysis")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")