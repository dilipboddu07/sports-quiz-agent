import streamlit as st

from src.database import setup_and_populate_db
from src.generator import compile_quiz_data


# -------------------------
# Initialize ChromaDB
# -------------------------

@st.cache_resource
def initialize_database():
    """
    Populate ChromaDB once.
    """
    return setup_and_populate_db()


initialize_database()


# -------------------------
# Streamlit Page Settings
# -------------------------

st.set_page_config(
    page_title="AI Sports Quiz Generator",
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 AI-Powered Sports Quiz Generator")

st.write(
    """
Generate sports quizzes using
Historical Facts (ChromaDB)
+
Live Internet News (DuckDuckGo)
+
Google Gemini
"""
)

# -------------------------
# Sidebar
# -------------------------

st.sidebar.header("Quiz Settings")

sport = st.sidebar.selectbox(
    "Choose Sport",
    (
        "Cricket",
        "Football",
        "Badminton"
    )
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    (
        "Easy",
        "Medium",
        "Hard"
    )
)

# -------------------------
# Session State
# -------------------------

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "context" not in st.session_state:
    st.session_state.context = None


# -------------------------
# Generate Quiz
# -------------------------

if st.sidebar.button(
    "Generate Quiz",
    use_container_width=True
):

    with st.spinner("Generating Quiz..."):

        try:

            quiz, context = compile_quiz_data(
                sport,
                difficulty
            )

            st.session_state.quiz = quiz
            st.session_state.context = context

            st.success("Quiz Generated Successfully!")

        except Exception as error:

            st.error(f"Error: {error}")


# -------------------------
# Display Quiz
# -------------------------

if st.session_state.quiz:

    st.subheader(
        f"{sport} Quiz ({difficulty})"
    )

    st.text_area(
        "Generated Quiz",
        value=st.session_state.quiz,
        height=350
    )

    with st.expander(
        "View RAG Context Used"
    ):

        st.code(
            st.session_state.context,
            language="text"
        )