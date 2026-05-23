import streamlit as st


def render():
    st.markdown('<h2 class="section-header">About PhishShield</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(0,245,255,0.04);border:1px solid rgba(0,245,255,0.12);border-radius:14px;padding:24px;margin-bottom:24px;">
        <p style="color:#c8cdd8;font-size:0.92rem;line-height:1.9;margin:0;">
            PhishShield is a supervised machine learning system designed to classify URLs as
            <strong style="color:#00f5a0;">legitimate</strong>,
            <strong style="color:#f5a623;">suspicious</strong>, or
            <strong style="color:#f54242;">phishing</strong>
            based on structural and behavioral URL features. It uses a Random Forest classifier
            trained on the UCI Phishing Websites dataset, achieving ~97% accuracy without
            requiring live network access.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset ──────────────────────────────────────────────────────
    st.markdown('<p class="section-header">📊 Dataset</p>', unsafe_allow_html=True)

    d1, d2 = st.columns([1, 1])
    with d1:
        info = [
            ("Source", "UCI ML Repository — Phishing Websites"),
            ("Total Samples", "5,849 unique URL records"),
            ("Feature Count", "30 binary/ternary features"),
            ("Class Distribution", "56% Legitimate · 44% Phishing"),
            ("Missing Values", "None — fully clean"),
            ("Feature Encoding", "-1 (phishing) · 0 (neutral) · 1 (legitimate)"),
        ]
        for key, val in info:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.85rem;">
                <span style="color:#8892a4;">{key}</span>
                <span style="color:#e8eaf0;font-weight:500;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;height:100%;">
            <p style="color:#8892a4;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">Feature Categories</p>
            <div style="display:grid;gap:8px;">
                <div style="background:rgba(0,245,255,0.06);border-radius:8px;padding:10px 14px;font-size:0.83rem;color:#c8cdd8;">
                    <strong style="color:#00f5ff;">Address Bar</strong> — IP, URL length, shortening, @, //, prefix-suffix, subdomains, HTTPS
                </div>
                <div style="background:rgba(168,85,247,0.06);border-radius:8px;padding:10px 14px;font-size:0.83rem;color:#c8cdd8;">
                    <strong style="color:#a855f7;">Domain</strong> — Registration length, age, DNS, favicon, non-standard port
                </div>
                <div style="background:rgba(0,245,160,0.06);border-radius:8px;padding:10px 14px;font-size:0.83rem;color:#c8cdd8;">
                    <strong style="color:#00f5a0;">HTML/JS</strong> — Request URL, anchor tags, script links, form handler, iframe
                </div>
                <div style="background:rgba(245,166,35,0.06);border-radius:8px;padding:10px 14px;font-size:0.83rem;color:#c8cdd8;">
                    <strong style="color:#f5a623;">External</strong> — Page rank, Google index, traffic, stats report
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Preprocessing ────────────────────────────────────────────────
    st.markdown('<p class="section-header">⚙️ Preprocessing Pipeline</p>', unsafe_allow_html=True)

    steps = [
        ("01", "Load Dataset", "Read the raw CSV from disk. Drop the index column which carries no predictive value."),
        ("02", "Deduplication", "Remove any duplicate rows to prevent training bias toward repeated examples."),
        ("03", "Label Encoding", "Remap class labels from {-1, 1} to {0, 1} for compatibility with sklearn's classifiers."),
        ("04", "Train/Test Split", "80/20 stratified split ensures balanced class representation in both sets."),
        ("05", "Feature Scaling", "StandardScaler normalizes each feature to zero mean and unit variance before training."),
        ("06", "Model Persistence", "Trained model and scaler are serialized with joblib for instant reuse."),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
        <div class="workflow-step">
            <div class="workflow-step-num">Step {num}</div>
            <div class="workflow-step-title">{title}</div>
            <div class="workflow-step-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Random Forest ────────────────────────────────────────────────
    st.markdown('<p class="section-header">🌲 Random Forest Classifier</p>', unsafe_allow_html=True)

    rf1, rf2 = st.columns(2)
    with rf1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌲</div>
            <div class="feature-title">Ensemble Learning</div>
            <div class="feature-desc">
                Random Forest builds many decision trees during training. Each tree votes on the outcome,
                and the majority vote determines the final prediction — reducing overfitting significantly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rf2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎲</div>
            <div class="feature-title">Feature Randomness</div>
            <div class="feature-desc">
                At each split, only a random subset of features is considered. This decorrelates
                the individual trees and makes the ensemble more robust to noise.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    rf3, rf4 = st.columns(2)
    with rf3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Feature Importance</div>
            <div class="feature-desc">
                After training, Random Forest reports Gini-based feature importances,
                revealing which URL characteristics are most predictive of phishing behavior.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rf4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Inference</div>
            <div class="feature-desc">
                Once trained, prediction is near-instant. No network requests or WHOIS lookups
                are needed — the classifier works purely from structural URL features.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Hyperparameters ──────────────────────────────────────────────
    with st.expander("🔧 Model Hyperparameters"):
        params = {
            "n_estimators": "200 trees",
            "max_depth": "None (fully grown)",
            "min_samples_split": "2",
            "min_samples_leaf": "1",
            "max_features": "sqrt(n_features)",
            "class_weight": "balanced",
            "random_state": "42 (reproducible)",
            "n_jobs": "-1 (all cores)",
        }
        for k, v in params.items():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.85rem;">
                <code style="color:#00f5ff;background:transparent;">{k}</code>
                <span style="color:#c8cdd8;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
