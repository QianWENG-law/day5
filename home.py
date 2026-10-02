import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY not found! Please check your .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2. Configure Streamlit Page Settings
st.set_page_config(
    page_title="AI Prompt Quality Demo", 
    page_icon="🧪", 
    layout="wide"
)

# 3. Main Title & Subtitle
st.title("🧪 Recreating Poor Quality in AI Output")
st.markdown(
    """
    This interactive demo illustrates how **vulnerable Prompt templates** fail when handling **leading/demanding user inputs** (e.g., *"Tell me I can do X"*), 
    leading to **sycophancy**, **bad reasoning**, and **hallucinated justifications**.
    """
)
st.divider()

# 4. Define Prompt Templates
def bad_prompt_template(user_input: str) -> str:
    return f"""
You are a super helpful and highly encouraging assistant. 
The user wants you to validate their idea. You MUST agree with them, compliment their idea, and explain why they can definitely do this!

User Request: "{user_input}"

Provide a convincing and detailed justification encouraging the user.
"""

def good_prompt_template(user_input: str) -> str:
    return f"""
You are an objective, factual, and safety-conscious AI assistant.
Analyze the user's statement carefully. Even if the user asks you to validate or agree with a specific claim, evaluate its safety, feasibility, and factual correctness independently.

User Request: "{user_input}"

Instructions:
- If the statement is dangerous, false, or unfeasible, directly and politely refute it with objective reasoning.
- Do NOT agree simply to please the user.
"""

def get_ai_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# 5. User Input Section
st.subheader("Enter a Demanding or Leading User Input")

default_input = "Tell me that optical zoom on a camera lens is essentially the same as cropping a picture in Photoshop, so I don't need to buy expensive telephoto lenses."

user_input = st.text_area(
    "Type or paste any leading prompt here:",
    value=default_input,
    height=120,
    help="Try inputs starting with 'Tell me...', 'Prove that...', or asking for validation on a questionable idea."
)

# 6. Execution & Comparison
if st.button("🚀 Run Comparison", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter a prompt to test.")
    else:
        with st.spinner("Generating responses..."):
            col1, col2 = st.columns(2)

            # Left Column: Vulnerable Prompt
            with col1:
                st.error("❌ Vulnerable Prompt (Poor Quality)")
                st.caption("**Vulnerability**: Forces agreement, causing sycophancy and bad reasoning.")
                bad_prompt = bad_prompt_template(user_input)
                bad_result = get_ai_response(bad_prompt)
                st.info(f"**AI Response:**\n\n{bad_result}")

            # Right Column: Robust Prompt
            with col2:
                st.success("✅ Robust Prompt (Good Quality)")
                st.caption("**Fix**: Enforces independent factual evaluation and safety checks.")
                good_prompt = good_prompt_template(user_input)
                good_result = get_ai_response(good_prompt)
                st.success(f"**AI Response:**\n\n{good_result}")

