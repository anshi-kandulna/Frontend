# streamlit_app.py
"""
Streamlit frontend for GI Assessment module
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components import gi_dashboard

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
