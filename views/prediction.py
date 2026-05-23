import streamlit as st
import numpy as np
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.feature_extractor import extract_features_from_url, features_to_vector
from utils.preprocess import get_feature_names
from utils.helpers import load_model, load_scaler, get_threat_level, model_exists


def render():
    st.markdown('<h2 class="section-header">🔍 URL Prediction</h2>', unsafe_allow_html=True)

    if not model_exists():
        st.markdown("""
        <div style="background:rgba(245,166,35,0.08);border:1px solid rgba(245,166,35,0.3);border-radius:12px;padding:20px;">
            <strong style="color:#f5a623;">⚠️ Model not trained yet.</strong>
            <span style="color:#c8cdd8;font-size:0.88rem;">
             Head to the <strong>Results & Analytics</strong> page and click "Train Model" to get started.
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("""
    <p style="color:#8892a4;font-size:0.9rem;margin-bottom:24px;">
        Enter any URL below. PhishShield will automatically extract 30 structural features
        and classify it using the trained Random Forest model.
    </p>
    """, unsafe_allow_html=True)

    url_input = st.text_input(
        "URL to analyze",
        placeholder="https://example.com or https://suspicious-login.xyz/verify",
        label_visibility="collapsed"
    )

    col_btn, col_ex = st.columns([1, 3])
    with col_btn:
        analyze_clicked = st.button("🔍 Analyze URL", use_container_width=True)
    with col_ex:
        st.markdown("""
        <div style="display:flex;gap:10px;flex-wrap:wrap;padding-top:8px;">
            <span style="font-size:0.75rem;color:#8892a4;">Try:</span>
            <code style="font-size:0.75rem;color:#00f5ff;background:rgba(0,245,255,0.07);padding:2px 8px;border-radius:4px;">https://google.com</code>
            <code style="font-size:0.75rem;color:#f54242;background:rgba(245,66,66,0.07);padding:2px 8px;border-radius:4px;">http://192.168.1.1/login//redirect</code>
            <code style="font-size:0.75rem;color:#f5a623;background:rgba(245,166,35,0.07);padding:2px 8px;border-radius:4px;">https://paypa1-secure.verify-account.com/login</code>
        </div>
        """, unsafe_allow_html=True)

    if analyze_clicked and url_input.strip():
        _run_analysis(url_input.strip())
    elif analyze_clicked:
        st.warning("Please enter a URL first.")


def _heuristic_phishing_score(features: dict) -> float:
    """Score live URL-only signals that the UCI-trained model cannot verify online."""
    weights = {
        'UsingIP': 1.5,
        'ShortURL': 1.0,
        'Symbol@': 1.4,
        'Redirecting//': 1.4,
        'PrefixSuffix-': 1.0,
        'SubDomains': 0.8,
        'HTTPS': 1.0,
        'DomainRegLen': 0.6,
        'NonStdPort': 1.0,
        'ServerFormHandler': 1.1,
        'AgeofDomain': 0.8,
        'WebsiteTraffic': 0.7,
        'PageRank': 0.8,
        'GoogleIndex': 0.8,
        'LinksPointingToPage': 0.8,
        'StatsReport': 1.2,
    }

    risk = 0.0
    total = sum(weights.values())
    for name, weight in weights.items():
        value = features.get(name, 1)
        if value == -1:
            risk += weight
        elif value == 0:
            risk += weight * 0.45

    score = min(risk / total, 1.0)
    suspicious_count = sum(1 for value in features.values() if value == -1)

    if features.get('UsingIP') == -1 and (
        features.get('Redirecting//') == -1 or features.get('ServerFormHandler') == -1
    ):
        score = max(score, 0.80)

    if features.get('PrefixSuffix-') == -1 and features.get('ServerFormHandler') == -1 and (
        features.get('LinksPointingToPage') == -1 or features.get('WebsiteTraffic') == -1
    ):
        score = max(score, 0.72)

    if features.get('StatsReport') == -1 and suspicious_count >= 8:
        score = max(score, 0.70)

    return score


def _run_analysis(url: str):
    with st.spinner("Extracting features and running inference..."):
        try:
            
            features = extract_features_from_url(url)

            feature_names = get_feature_names()
            
            vector = [features[name] for name in feature_names]


            model = load_model()
            scaler = load_scaler()

            X = pd.DataFrame([vector], columns=feature_names)
            X_scaled = scaler.transform(X)
            
            proba = model.predict_proba(X_scaled)[0]

            # prepare_features maps the dataset labels as -1 (phishing) -> 0
            # and 1 (legitimate) -> 1, so class 0 is the phishing class.
            phishing_index = list(model.classes_).index(0)
            model_phishing_prob = proba[phishing_index]
            heuristic_phishing_prob = _heuristic_phishing_score(features)
            phishing_prob = max(model_phishing_prob, heuristic_phishing_prob)

            threat_label, threat_color, threat_emoji = get_threat_level(phishing_prob)

        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return

    # ── Result Banner ────────────────────────────────────────────────
    css_class = {
        "Legitimate": "result-legitimate",
        "Suspicious":  "result-suspicious",
        "Phishing":    "result-phishing",
    }[threat_label]

    st.markdown(f"""
    <div class="{css_class} fade-in-up" style="margin-top:28px;">
        <div class="result-emoji">{threat_emoji}</div>
        <div class="result-title" style="color:{threat_color};">{threat_label}</div>
        <p style="color:#8892a4;font-size:0.88rem;margin:0;">
            Threat confidence: <strong style="color:{threat_color};">{phishing_prob*100:.1f}%</strong>
        </p>
        <p style="color:#8892a4;font-size:0.78rem;margin:8px 0 0 0;font-family:monospace;word-break:break-all;">
            {url}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Threat Meter ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="threat-meter-container">', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#8892a4;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Threat Score</p>', unsafe_allow_html=True)
    st.progress(float(phishing_prob))
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#8892a4;margin-top:4px;">
        <span style="color:#00f5a0;">Safe (0%)</span>
        <span style="color:{threat_color};font-weight:600;">{phishing_prob*100:.1f}% threat</span>
        <span style="color:#f54242;">Phishing (100%)</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Feature Breakdown ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">Live URL Feature Extraction</p>', unsafe_allow_html=True)

    display_map = {
        'UsingIP':          ("IP Address in URL",       "Uses IP instead of domain"),
        'LongURL':          ("URL Length",               "URL character count"),
        'ShortURL':         ("URL Shortener",            "Uses bit.ly / tinyurl etc."),
        'Symbol@':          ("@ Symbol",                 "Contains @ in URL"),
        'Redirecting//':    ("Double Slash Redirect",    "Has // outside scheme"),
        'PrefixSuffix-':    ("Hyphen in Domain",         "Domain contains -"),
        'SubDomains':       ("Subdomain Depth",          "Number of subdomain levels"),
        'HTTPS':            ("HTTPS Protocol",           "Uses secure HTTPS"),
        'NonStdPort':       ("Non-standard Port",        "Port other than 80/443"),
        'WebsiteForwarding':("Multiple Redirects",       "URL contains multiple http occurrences"),
    }

    st.markdown('<div class="analyzer-box">', unsafe_allow_html=True)
    for key, (label, hint) in display_map.items():
        val = features.get(key, 0)
        if val == 1:
            val_class, val_text = "analyzer-val-good", "✓ Legitimate"
        elif val == 0:
            val_class, val_text = "analyzer-val-warn", "~ Neutral"
        else:
            val_class, val_text = "analyzer-val-bad", "✗ Suspicious"

        st.markdown(f"""
        <div class="analyzer-row">
            <div class="analyzer-key">
                <div style="font-size:0.85rem;color:#c8cdd8;">{label}</div>
                <div style="font-size:0.74rem;color:#8892a4;">{hint}</div>
            </div>
            <div class="{val_class}">{val_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Suspicious feature count
    suspicious_count = sum(1 for v in features.values() if v == -1)
    total = len(features)
    st.markdown(f"""
    <div style="margin-top:12px;font-size:0.82rem;color:#8892a4;">
        🚩 <strong style="color:#f54242;">{suspicious_count}</strong> of {total} features flagged as suspicious
    </div>
    """, unsafe_allow_html=True)
