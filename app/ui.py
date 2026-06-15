import streamlit as st
import requests
import os

# Configure page layout and style
st.set_page_config(page_title="Semantic Discovery Engine", layout="centered")

st.title("📸 LensMind")
st.subheader("AI-Powered Semantic Discovery for Photographers")
st.write("Describe *how* or *what* you want to shoot in plain human language. Our vector database will map your creative intent to the perfect gear infrastructure.")

# Debug: Show backend URL.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# 1. Search Interface Input Element
user_query = st.text_input(
    label="Creative Intent Query",
    placeholder="e.g., I want to capture intimate street portraits at night with soft background bokeh...",
    label_visibility="collapsed"
)

search_button = st.button("Discover Gear", type="primary")

# 2. Connection to FastAPI Backend Trigger
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
            
            # 3. Dynamic Results Render Matrix
            for idx, item in enumerate(search_results):
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {item['name']}")
                    st.caption(f"📁 {item['category']} | 🛠️ Specs: {item['specs']}")
                
                with col2:
                    # Render the cosine similarity confidence score metric
                    st.metric(label="Vector Match", value=f"{item['confidence_score']:.4f}")
                
                st.write(item['description'])
                
        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to FastAPI Backend Services: {str(e)}")