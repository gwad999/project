"""
Run this script once to train and save the model:
    python train_model.py
It saves two files into models/:
    - phishing_model.pkl   (Random Forest classifier)
    - scaler.pkl           (StandardScaler fitted on training data)
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.preprocess import load_data, prepare_features, split_and_scale
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Loading dataset...")
df = load_data()
X, y = prepare_features(df)
print(f"  {len(df)} samples, {X.shape[1]} features")

print("Splitting and scaling...")
X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)
print(f"  Train: {len(X_train)}  |  Test: {len(X_test)}")

print("Training Random Forest (200 trees)...")
model = RandomForestClassifier(
    n_estimators=200,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\nAccuracy : {accuracy_score(y_test, y_pred)*100:.2f}%")
print(classification_report(y_test, y_pred, target_names=['Phishing', 'Legitimate']))

joblib.dump(model,  'models/phishing_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("Saved: models/phishing_model.pkl")
print("Saved: models/scaler.pkl")
print("\nDone. Now run:  streamlit run app.py")
