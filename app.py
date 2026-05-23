import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from views import about, home, prediction, results

st.set_page_config(
    page_title="PhishShield - AI Phishing Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

PAGES = {
    "Home": home.render,
    "About": about.render,
    "Prediction": prediction.render,
    "Results & Analytics": results.render,
}

st.markdown(
    """
    <div class="top-nav-spacer"></div>
    """,
    unsafe_allow_html=True,
)

brand_col, nav_col = st.columns([1.05, 2.95], vertical_alignment="center")
with brand_col:
    st.markdown(
        """
        <div class="top-nav-brand">
            <span class="top-nav-logo">🛡️</span>
            <span>
                <span class="top-nav-title">PhishShield</span>
                <span class="top-nav-subtitle">AI Phishing Detector</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col:
    page_key = st.segmented_control(
        "Navigation",
        options=list(PAGES.keys()),
        default="Home",
        label_visibility="collapsed",
        key="top_navigation",
    )

if page_key is None:
    page_key = "Home"

PAGES[page_key]()
