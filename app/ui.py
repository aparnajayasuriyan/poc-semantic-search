import os

import requests
import streamlit as st

# Configure page layout and style
st.set_page_config(page_title="LensMind", layout="wide")

page_bg = "#f6f6f6"
card_bg = "#ffffff"
text_color = "#111111"
muted_color = "#6e6e73"
primary_color = "#0a84ff"

st.markdown(
    f"""
    <style>
    .css-2trqyj {{padding: 0 !important;}}
    .css-1v0mbdj {{padding: 0 !important;}}
    .css-1lcbmhc {{background-color: {page_bg};}}
    .css-1v0mbdj, .css-2trqyj, .css-1j3t6r9 {{
        background-color: #f2f2f2 !important;
        color: {text_color} !important;
    }}
    .stApp {{
        background-color: {page_bg};
        color: {text_color};
    }}
    .stButton>button {{
        background-color: {primary_color};
        color: #ffffff;
        border-radius: 999px;
        padding: 0.8rem 1.6rem;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 20px rgba(10, 132, 255, 0.18);
        transition: transform 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease;
    }}
    .stButton>button:hover {{
        background-color: #3b82f6;
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(10, 132, 255, 0.22);
    }}
    .stTextInput, .stTextInput>div, .stTextInput>div>div {{
        border-radius: 24px !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}
    .stTextInput input, .stTextInput>div>div>input {{
        border-radius: 24px !important;
        padding: 1rem 1.25rem;
        border: 1px solid #d6d6d8;
        background-color: #ffffff;
        color: {text_color};
        font-size: 1rem;
        opacity: 1;
        outline: none;
        box-shadow: none;
    }}
    .stTextInput input:focus, .stTextInput>div>div>input:focus {{
        border-color: #0a84ff;
        box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.12);
    }}
    .stTextInput input::placeholder, .stTextInput>div>div>input::placeholder {{
        color: #8e8e93 !important;
        opacity: 1 !important;
    }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: {text_color};
    }}
    .stMarkdown p, .stMarkdown span {{
        color: {muted_color};
    }}
    .result-card {{
        border-radius: 24px;
        background: {card_bg};
        padding: 1.8rem;
        box-shadow: 0px 24px 60px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }}
    .result-meta {{
        color: {muted_color};
        font-size: 0.94rem;
        line-height: 1.6;
    }}
    .price-tag {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        background: rgba(10, 132, 255, 0.12);
        color: {primary_color};
        font-weight: 700;
        font-size: 0.95rem;
    }}
    .streamlit-expanderHeader {{ font-weight: 600; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# LensMind")
st.markdown("### Discover the right camera gear with a more intuitive, polished search experience.")
st.markdown(
    "Describe your shoot, mood, or workflow and LensMind maps that intent to camera bodies, lenses, lighting, and accessories."
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

query_col, empty_col = st.columns([3, 1])
with query_col:
    user_query = st.text_input(
        label="Search",
        placeholder="e.g., cinematic night portraits with soft backlight and shallow depth of field",
        label_visibility="collapsed",
    )
    st.markdown("---")
    search_button = st.button("Discover Gear")

if search_button and user_query:
    API_URL = f"{BACKEND_URL}/api/v1/discover"
    payload = {"query": user_query, "limit": 3}

    with st.spinner("Analyzing semantic vector proximity..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            search_results = response.json().get("results", [])

            if not search_results:
                st.info("No matching gear vectors found for that specific description.")

            for item in search_results:
                st.markdown(
                    f"<div class='result-card'>",
                    unsafe_allow_html=True,
                )
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {item['name']}")
                    price = item.get('price')
                    price_text = f"${price:.2f}" if isinstance(price, (int, float)) else "N/A"
                    st.markdown(
                        f"<div class='result-meta'>📁 {item['category']} | 🛠️ {item['specs']} &nbsp;&nbsp; <span class='price-tag'>{price_text}</span></div>",
                        unsafe_allow_html=True,
                    )
                    st.write(item['description'])

                with col2:
                    st.metric(label="Vector Match", value=f"{item['confidence_score']:.4f}")

                st.markdown("</div>", unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to FastAPI Backend Services: {str(e)}")
