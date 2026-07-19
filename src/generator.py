import google.generativeai as genai

from src.config import GEMINI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context


# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def compile_quiz_data(sport, difficulty):
    """
    Performs the complete RAG pipeline.

    Steps:
    1. Retrieve historical facts from ChromaDB.
    2. Retrieve live news from DuckDuckGo.
    3. Merge both contexts.
    4. Generate quiz using Gemini.
    """

    # -------------------------
    # Retrieve historical facts
    # -------------------------

    db_query = f"{sport} history championships rules records"

    db_matches = query_historic_facts(
        sport=sport,
        query_text=db_query,
        n_results=2
    )

    if db_matches:
        db_context = "\n".join(db_matches)
    else:
        db_context = "No historical information available."

    # -------------------------
    # Retrieve live news
    # -------------------------

    web_context = get_live_news_context(sport)

    # -------------------------
    # Combine both contexts
    # -------------------------

    combined_context = f"""
========== HISTORICAL FACTS ==========

{db_context}

========== LIVE SPORTS NEWS ==========

{web_context}
"""

    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
You are an expert Sports Quiz Generator.

STRICT RULES:

1. ONLY use the provided context.
2. Never invent facts.
3. Generate exactly THREE multiple-choice questions.
4. Difficulty: {difficulty}
5. Sport: {sport}

Each question MUST follow this format:

Question:
A)
B)
C)
D)

Correct Answer:

Explanation:

Context:

====================

CONTEXT

{combined_context}
"""

    # -------------------------
    # Gemini Model
    # -------------------------

    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(prompt)

    quiz_text = response.text

    return quiz_text, combined_context