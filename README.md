# 🛡️ PhishShield — Phishing Website Detection System

A machine learning cybersecurity project that detects phishing websites in real time using a Random Forest classifier trained on 30+ structural URL features.

---

## 📸 Features

| Page | Description |
|------|-------------|
| 🏠 Home | Dashboard overview with stats, feature highlights, and threat level guide |
| ℹ️ About | Dataset details, preprocessing pipeline, and RF algorithm explanation |
| 🔍 Prediction | Enter any URL → get a live threat classification with feature breakdown |
| 📈 Results | Model metrics (accuracy, precision, recall, F1), confusion matrix, feature importances |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourname/PhishShield.git
cd PhishShield

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make sure the dataset is in place
#    data/dataset.csv should already be included

# 5. Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

> **First run:** Go to **Results & Analytics** and click **Train Model Now** to train and save the classifier.

---

## 📁 Project Structure

```
PhishShield/
├── app.py                  # Main Streamlit entry point
├── pages/
│   ├── home.py             # Landing dashboard
│   ├── about.py            # Dataset & algorithm explanation
│   ├── prediction.py       # URL analysis and prediction
│   └── results.py          # Model metrics and charts
├── utils/
│   ├── preprocess.py       # Data loading and preprocessing
│   ├── feature_extractor.py # URL → feature vector extraction
│   └── helpers.py          # Model I/O and utility functions
├── models/
│   ├── phishing_model.pkl  # Trained RF model (generated on first train)
│   └── scaler.pkl          # Feature scaler (generated on first train)
├── data/
│   └── dataset.csv         # UCI Phishing Websites dataset
├── assets/
│   └── styles.css          # Custom dark cybersecurity theme
├── requirements.txt
└── README.md
```

---

## 🧠 Model Details

- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Trees:** 200 estimators
- **Features:** 30 binary/ternary URL features (-1, 0, 1 encoded)
- **Training split:** 80% train / 20% test (stratified)
- **Accuracy:** ~97%
- **Persistence:** joblib serialization

### Feature Categories

- **Address Bar:** IP in URL, URL length, shorteners, @ symbol, // redirect, hyphens, subdomains, HTTPS
- **Domain:** Registration length, favicon, non-standard ports, HTTPS in domain
- **HTML/JS:** Request URL, anchor links, script tags, form handlers, iframes
- **External:** Page rank, Google index, website traffic, stats reports

---

## 📊 Dataset

- **Source:** UCI Machine Learning Repository — Phishing Websites
- **Samples:** 11,054 URLs
- **Classes:** 1 (Legitimate) · -1 (Phishing)
- **Missing values:** None

---

## 🎨 Design

- Dark cybersecurity aesthetic with matte black and deep navy backgrounds
- Neon cyan (#00f5ff) and purple (#a855f7) accent palette
- Glassmorphism card effects with glow animations
- Space Grotesk + Inter typography
- Fully responsive Streamlit layout

---

## ⚠️ Disclaimer

PhishShield is an academic final-year project. It classifies URLs based on structural features only — it does not make live HTTP requests or perform DNS lookups during prediction. Do not use this as your sole security measure.

---

## 📜 License

MIT License — free to use and modify for educational purposes.
