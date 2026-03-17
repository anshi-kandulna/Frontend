# streamlit_app.py
"""
Streamlit frontend for GI Assessment module
Run with: streamlit run streamlit_app.py
"""

import streamlit as st

from .component import gi_dashboard

# Configure page
st.set_page_config(
    page_title="GI Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
if __name__ == "__main__":
    gi_dashboard()
