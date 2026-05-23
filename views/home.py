import streamlit as st


def render():
    st.markdown("""
    <div class="hero-section fade-in-up">
        <p style="font-size:0.75rem;color:#00f5ff;text-transform:uppercase;letter-spacing:0.15em;font-weight:600;margin-bottom:10px;">
            🛡️ AI-Powered Cybersecurity
        </p>
        <h1 class="hero-title">PhishShield</h1>
        <p class="hero-subtitle">
            A machine learning system that detects phishing websites in real time using
            Random Forest classification trained on 30+ behavioral and structural URL features.
        </p>
        <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap;">
            <span style="background:rgba(0,245,255,0.1);border:1px solid rgba(0,245,255,0.3);padding:6px 16px;border-radius:20px;font-size:0.8rem;color:#00f5ff;">
                Random Forest
            </span>
            <span style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.3);padding:6px 16px;border-radius:20px;font-size:0.8rem;color:#a855f7;">
                Real-time Detection
            </span>
            <span style="background:rgba(0,245,160,0.1);border:1px solid rgba(0,245,160,0.3);padding:6px 16px;border-radius:20px;font-size:0.8rem;color:#00f5a0;">
                11,000+ Training Samples
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Stats Row ---
    st.markdown('<p class="section-header">At a Glance</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (c1, "5,849", "Unique Samples"),
        (c2, "30", "URL Features"),
        (c3, "~94%", "Model Accuracy"),
        (c4, "3", "Threat Levels"),
    ]
    for col, val, label in stats:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Feature Highlights ---
    st.markdown('<p class="section-header">What PhishShield Detects</p>', unsafe_allow_html=True)

    features = [
        ("🔗", "IP-Based URLs", "Detects when a numeric IP address is used instead of a domain name — a classic phishing indicator."),
        ("🔒", "HTTPS Verification", "Checks for the presence and legitimacy of SSL/TLS encryption on the site."),
        ("📏", "URL Length Analysis", "Abnormally long URLs are a known obfuscation technique used by phishing sites."),
        ("🚩", "Suspicious Symbols", "Flags the presence of @ symbols, double slashes, and redirect patterns."),
        ("🌐", "Subdomain Depth", "Analyzes subdomain nesting — deeply nested subdomains are often malicious."),
        ("⚡", "Redirect Patterns", "Identifies chained URL redirects used to mask the final malicious destination."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # --- Threat Level Overview ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">Threat Classification</p>', unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div style="background:rgba(0,245,160,0.06);border:1px solid rgba(0,245,160,0.3);border-radius:14px;padding:24px;text-align:center;">
            <div style="font-size:2rem;">✅</div>
            <div style="font-size:1rem;font-weight:700;color:#00f5a0;margin:8px 0;">Legitimate</div>
            <div style="font-size:0.8rem;color:#8892a4;">URL exhibits no known phishing characteristics. Safe to proceed.</div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div style="background:rgba(245,166,35,0.06);border:1px solid rgba(245,166,35,0.3);border-radius:14px;padding:24px;text-align:center;">
            <div style="font-size:2rem;">⚠️</div>
            <div style="font-size:1rem;font-weight:700;color:#f5a623;margin:8px 0;">Suspicious</div>
            <div style="font-size:0.8rem;color:#8892a4;">Some warning signs detected. Proceed with caution.</div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div style="background:rgba(245,66,66,0.07);border:1px solid rgba(245,66,66,0.35);border-radius:14px;padding:24px;text-align:center;">
            <div style="font-size:2rem;">🚨</div>
            <div style="font-size:1rem;font-weight:700;color:#f54242;margin:8px 0;">Phishing</div>
            <div style="font-size:0.8rem;color:#8892a4;">High-confidence phishing site detected. Do not visit.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px 24px;">
        <p style="color:#8892a4;font-size:0.82rem;margin:0;line-height:1.8;">
            ⚠️ <strong style="color:#e8eaf0;">Disclaimer:</strong>
            PhishShield is an academic machine learning project. Predictions are based on structural URL features
            and should not be used as the sole security measure. Always verify URLs through official channels.
        </p>
    </div>
    """, unsafe_allow_html=True)
