import os
import streamlit as st
import pandas as pd
import re
from dotenv import load_dotenv
from utils import load_career_data, get_career_matches

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

st.set_page_config(page_title="🤖 Career & Chat Assistant", layout="centered")
st.title("🤖 Career & Chat Assistant")

try:
    careers = load_career_data("careers.json")
except FileNotFoundError:
    st.error("❌ careers.json file not found.")
    st.stop()

# Initialize chat history and results in session_state
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "ai", "content": "👋 Hi! Tell me your interests or ask me any career question!"}
    ]
if "results" not in st.session_state:
    st.session_state.results = []
if "results_shown" not in st.session_state:
    st.session_state.results_shown = 0
RESULTS_BATCH_SIZE = 5

def clean_input(text):
    """Basic input cleaning."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def color_score(score):
    """Return color code based on confidence score."""
    if score > 0.75:
        return "green"
    elif score > 0.5:
        return "orange"
    else:
        return "red"

# Display previous chat messages
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your interests or career questions here...")

if user_input:
    user_input = clean_input(user_input)
    if not user_input:
        st.warning("Please enter a valid message.")
    else:
        st.session_state.chat.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("ai"):
            if not COHERE_API_KEY:
                reply = "❌ Cohere API key missing. Please set COHERE_API_KEY in your environment."
                st.error(reply)
                st.session_state.chat.append({"role": "ai", "content": reply})
            else:
                # Show typing spinner
                with st.spinner("Searching for career matches..."):
                    try:
                        results = get_career_matches(user_input, careers, COHERE_API_KEY, min_score=0.3)
                        st.session_state.results = results
                        st.session_state.results_shown = 0

                        if results:
                            MIN_CONFIDENCE = 0.45

                            # Separate strong matches and less relevant ones
                            strong_matches = [r for r in results if r['score'] >= MIN_CONFIDENCE]
                            less_relevant = [r for r in results if r['score'] < MIN_CONFIDENCE]

                            def format_career(r, highlight=False):
                                title = r['title']
                                if highlight:
                                    title = f"**🌟 {title}**"  # star for exact match
                                score_color = color_score(r['score'])
                                return (
                                    f"{title}\n"
                                    f"Description: {r['description']}\n"
                                    f"Tags: {', '.join(r['tags'])}\n"
                                    f"<span style='color:{score_color}'>Confidence Score: {r['score']}</span>\n\n"
                                )

                            user_lower = user_input.strip().lower()
                            reply = f"✅ Found {len(strong_matches)} career options you might like:\n\n"

                            # Highlight exact matches first
                            for r in strong_matches:
                                highlight = (r['title'].lower() == user_lower)
                                reply += format_career(r, highlight=highlight)

                            if less_relevant:
                                reply += "⚠️ Some less relevant options (lower confidence):\n\n"
                                for r in less_relevant:
                                    reply += format_career(r)
                        else:
                            reply = "🤔 I couldn’t find strong career matches for your input. Try mentioning skills, fields, or industries."

                        st.markdown(reply, unsafe_allow_html=True)
                        st.session_state.chat.append({"role": "ai", "content": reply})
                        st.session_state.results_shown = RESULTS_BATCH_SIZE
                    except Exception as e:
                        error_msg = f"⚠️ Something went wrong: {e}"
                        st.error(error_msg)
                        st.session_state.chat.append({"role": "ai", "content": error_msg})

# Load More button to show more results in chat
if st.session_state.results and st.session_state.results_shown < len(st.session_state.results):
    if st.button(f"Load more results ({len(st.session_state.results) - st.session_state.results_shown} left)"):
        with st.chat_message("ai"):
            next_batch = st.session_state.results[st.session_state.results_shown:st.session_state.results_shown + RESULTS_BATCH_SIZE]
            reply = ""
            for r in next_batch:
                reply += (
                    f"**💼 {r['title']}**\n"
                    f"Description: {r['description']}\n"
                    f"Tags: {', '.join(r['tags'])}\n"
                    f"<span style='color:{color_score(r['score'])}'>Confidence Score: {r['score']}</span>\n\n"
                )
            st.markdown(reply, unsafe_allow_html=True)
            st.session_state.chat.append({"role": "ai", "content": reply})
            st.session_state.results_shown += RESULTS_BATCH_SIZE

# Export button to download results as CSV
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download career matches as CSV",
        data=csv,
        file_name='career_matches.csv',
        mime='text/csv',
    )
