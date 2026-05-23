import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
import joblib
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.preprocess import load_data, prepare_features, split_and_scale, get_feature_names
from utils.helpers import model_exists

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#8892a4', family='Inter'),
    margin=dict(l=20, r=20, t=40, b=20),
)


def render():
    st.markdown('<h2 class="section-header">📈 Results & Analytics</h2>', unsafe_allow_html=True)

    # ── Train Button ─────────────────────────────────────────────────
    if not model_exists():
        st.markdown("""
        <div style="background:rgba(0,245,255,0.04);border:1px solid rgba(0,245,255,0.15);border-radius:12px;padding:20px 24px;margin-bottom:24px;">
            <p style="color:#c8cdd8;margin:0;font-size:0.9rem;">
                No trained model found. Click below to train the Random Forest classifier on the dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Train Model Now", use_container_width=False):
            _train_and_cache()
            st.rerun()
        return

    # ── Load Cached Metrics ──────────────────────────────────────────
    if 'metrics' not in st.session_state:
        _train_and_cache()

    metrics = st.session_state.get('metrics', {})
    if not metrics:
        st.error("Metrics unavailable. Please retrain the model.")
        if st.button("🔄 Retrain"):
            _train_and_cache()
            st.rerun()
        return

    col_r, _ = st.columns([1, 4])
    with col_r:
        if st.button("🔄 Retrain Model"):
            _train_and_cache()
            st.rerun()

    # ── KPI Row ──────────────────────────────────────────────────────
    st.markdown('<p class="section-header" style="margin-top:20px;">Model Performance</p>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "Accuracy",  f"{metrics['accuracy']*100:.2f}%"),
        (k2, "Precision", f"{metrics['precision']*100:.2f}%"),
        (k3, "Recall",    f"{metrics['recall']*100:.2f}%"),
        (k4, "F1-Score",  f"{metrics['f1']*100:.2f}%"),
    ]
    for col, label, val in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confusion Matrix + Feature Importance ────────────────────────
    left, right = st.columns(2)

    with left:
        st.markdown('<p style="color:#8892a4;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Confusion Matrix</p>', unsafe_allow_html=True)
        cm = np.array(metrics['confusion_matrix'])
        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted Phishing', 'Predicted Legitimate'],
            y=['Actual Phishing', 'Actual Legitimate'],
            colorscale=[[0, '#0a0e1a'], [0.5, '#7c3aed'], [1, '#00f5ff']],
            text=cm, texttemplate="%{text}",
            textfont=dict(size=18, color='white'),
            showscale=False,
        ))
        fig_cm.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
            xaxis=dict(side='bottom'),
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    with right:
        st.markdown('<p style="color:#8892a4;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Top 10 Feature Importances</p>', unsafe_allow_html=True)
        importances = metrics['feature_importances']
        feat_names = metrics['feature_names']

        top_idx = np.argsort(importances)[-10:][::-1]
        top_feats = [feat_names[i] for i in top_idx]
        top_vals  = [importances[i] for i in top_idx]

        fig_fi = go.Figure(go.Bar(
            x=top_vals,
            y=top_feats,
            orientation='h',
            marker=dict(
                color=top_vals,
                colorscale=[[0, '#7c3aed'], [1, '#00f5ff']],
            ),
        ))
        fig_fi.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
            yaxis=dict(autorange='reversed'),
            xaxis=dict(title='Importance'),
        )
        st.plotly_chart(fig_fi, use_container_width=True)

    # ── Class Distribution ───────────────────────────────────────────
    st.markdown('<p class="section-header">Dataset Overview</p>', unsafe_allow_html=True)
    dist_col, roc_col = st.columns(2)

    with dist_col:
        st.markdown('<p style="color:#8892a4;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Class Distribution</p>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Legitimate', 'Phishing'],
            values=[2830, 3019],
            hole=0.55,
            marker=dict(colors=['#00f5a0', '#f54242'], line=dict(color='#0a0e1a', width=2)),
            textfont=dict(size=13),
        ))
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=True,
                               legend=dict(orientation='h', y=-0.1))
        fig_pie.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with roc_col:
        st.markdown('<p style="color:#8892a4;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">All Feature Importances</p>', unsafe_allow_html=True)
        sorted_idx = np.argsort(importances)[::-1]
        fig_all = go.Figure(go.Bar(
            x=[feat_names[i] for i in sorted_idx],
            y=[importances[i] for i in sorted_idx],
            marker=dict(color='#a855f7', opacity=0.8),
        ))
        fig_all.update_layout(
            **PLOTLY_LAYOUT,
            height=280,
            xaxis=dict(tickangle=-45, tickfont=dict(size=8)),
        )
        st.plotly_chart(fig_all, use_container_width=True)

    # ── Classification Report ────────────────────────────────────────
    with st.expander("📄 Full Classification Report"):
        report_df = pd.DataFrame(metrics['classification_report']).T
        report_df = report_df.drop(index=['accuracy'], errors='ignore')
        report_df = report_df.round(4)
        st.dataframe(
            report_df.style.background_gradient(cmap='Blues', subset=['f1-score']),
            use_container_width=True
        )


def _train_and_cache():
    with st.spinner("Loading data and training Random Forest... this takes a few seconds."):
        df = load_data()
        X, y = prepare_features(df)
        X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)

        model = RandomForestClassifier(
            n_estimators=200,
            max_features='sqrt',
            class_weight='balanced',
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)

        joblib.dump(model, os.path.join(MODEL_DIR, 'phishing_model.pkl'))

        y_pred = model.predict(X_test)

        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        st.session_state['metrics'] = {
            'accuracy':             accuracy_score(y_test, y_pred),
            'precision':            precision_score(y_test, y_pred, average='weighted'),
            'recall':               recall_score(y_test, y_pred, average='weighted'),
            'f1':                   f1_score(y_test, y_pred, average='weighted'),
            'confusion_matrix':     cm.tolist(),
            'feature_importances':  model.feature_importances_.tolist(),
            'feature_names':        get_feature_names(),
            'classification_report': report,
        }

    st.success("✅ Model trained and saved successfully!")
