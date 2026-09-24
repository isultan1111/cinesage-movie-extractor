import os

import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field
from typing import List, Optional

from langchain_core.output_parsers import PydanticOutputParser


# =========================================================
# 1. CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="CineSage - Movie Extractor",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# 2. CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #1e1b4b 100%
        );
    }

    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        color: white;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }

    .info-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 25px;
        margin-top: 20px;
        backdrop-filter: blur(10px);
    }

    .section-title {
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.2rem;
        font-size: 1.1rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(
            90deg,
            #7c3aed,
            #4f46e5
        );
        color: white;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #6366f1
        );
        color: white;
    }

    textarea {
        border-radius: 14px !important;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 40px;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎬 CineSage</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered movie information extractor using LangChain + Groq'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 4. PYDANTIC MODELS
# =========================================================

class Movie(BaseModel):

    title: str

    release_year: Optional[int] = None

    genre: List[str] = Field(
        default_factory=list
    )

    director: Optional[str] = None

    cast: List[str] = Field(
        default_factory=list
    )

    rating: Optional[float] = None

    summary: str = ""
    
class Movies(BaseModel):

    movies: List[Movie]


# =========================================================
# 5. OUTPUT PARSER
# =========================================================

parser = PydanticOutputParser(
    pydantic_object=Movies
)


# =========================================================
# 6. GROQ CONFIGURATION
# =========================================================

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:

    st.error(
        "❌ GROQ_API_KEY not found. "
        "Please add GROQ_API_KEY to your .env file."
    )

    st.stop()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=groq_api_key
)


# =========================================================
# 7. PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages(
    [

        (
            "system",
            """
You are CineSage, an AI movie information extraction system.

Your task is to extract ALL movies mentioned in the
provided paragraph.

IMPORTANT RULES:

1. Extract every distinct movie mentioned.

2. Create exactly ONE Movie object for each movie.

3. Do not skip any movie.

4. Do not combine multiple movies into one object.

5. Only use information supported by the provided text.

6. Do not invent information.

7. If release year is unavailable, use null.

8. If director is unavailable, use null.

9. If rating is unavailable, use null.

10. If genre is unavailable, use [].

11. If cast is unavailable, use [].

12. If summary is unavailable, create a short summary
    ONLY from information available in the paragraph.

13. Every movie object MUST contain:
    - title
    - release_year
    - genre
    - director
    - cast
    - rating
    - summary

14. NEVER create an empty movie object.

15. NEVER create an object with an empty title.

16. Do not create extra movie objects.

17. Return ONLY valid JSON.

18. Do not return markdown.

19. Do not return ```json.

20. Do not add explanations before or after the JSON.

21.User can input multiple movie without sepration diffentiate movie and then genrate.

22.22. Before returning JSON, verify that EVERY movie object contains
    all 7 required fields. If any field is missing, add it using
    null, [], or "" according to the field type.

Required format:

{format_instruction}
"""
        ),

        (
            "human",
            "{paragraph}"
        )

    ]
)


# =========================================================
# 8. INPUT SECTION
# =========================================================

st.markdown(
    '<div class="info-card">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">'
    '📝 Enter Movie Information'
    '</div>',
    unsafe_allow_html=True
)

paragraph = st.text_area(
    "Movie paragraph",

    placeholder=(
        "Example:\n\n"
        "The Dark Knight is a 2008 superhero crime film "
        "directed by Christopher Nolan. It stars Christian Bale "
        "and Heath Ledger. Inception is a 2010 science fiction "
        "film directed by Christopher Nolan and stars Leonardo "
        "DiCaprio."
    ),

    height=250,

    label_visibility="collapsed"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# 9. EXTRACT BUTTON
# =========================================================

st.write("")


if st.button("🎬 Extract Movie Information"):

    # -----------------------------------------------------
    # Check input
    # -----------------------------------------------------

    if not paragraph.strip():

        st.warning(
            "⚠️ Please enter a movie paragraph first."
        )

    else:

        with st.spinner(
            "🤖 Extracting movie information..."
        ):

            try:

                # -------------------------------------------------
                # Create final prompt
                # -------------------------------------------------

                final_prompt = prompt.invoke(
                    {
                        "paragraph": paragraph,

                        "format_instruction":
                            parser.get_format_instructions()
                    }
                )


                # -------------------------------------------------
                # Send request to Groq
                # -------------------------------------------------

                response = llm.invoke(
                    final_prompt
                )


                # -------------------------------------------------
                # Parse response
                # -------------------------------------------------

                movies = parser.parse(
                    response.content
                )


                # -------------------------------------------------
                # Validate movies
                # -------------------------------------------------

                valid_movies = []

                for movie in movies.movies:

                    # Ignore accidental empty movie objects
                    if movie.title.strip():

                        valid_movies.append(
                            movie
                        )


                # Create final object
                movies = Movies(
                    movies=valid_movies
                )


                # -------------------------------------------------
                # Convert to JSON
                # -------------------------------------------------

                json_output = movies.model_dump_json(
                    indent=4
                )


                # -------------------------------------------------
                # Success
                # -------------------------------------------------

                st.success(
                    f"Found {len(movies.movies)} movie(s)"
                )


                # =================================================
                # 10. JSON OUTPUT
                # =================================================

                st.markdown(
                    '<div class="info-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="section-title">'
                    '📦 JSON Output'
                    '</div>',
                    unsafe_allow_html=True
                )


                # Display JSON
                st.json(
                    movies.model_dump()
                )


                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


                # =================================================
                # 11. DOWNLOAD JSON
                # =================================================

                st.download_button(

                    label="⬇️ Download JSON",

                    data=json_output,

                    file_name="movies.json",

                    mime="application/json"
                )


            # =====================================================
            # ERROR HANDLING
            # =====================================================

            except Exception as e:

                st.error(
                    f"❌ Error: {e}"
                )


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Built with ❤️ using Streamlit • LangChain • Groq'
    '</div>',
    unsafe_allow_html=True
)