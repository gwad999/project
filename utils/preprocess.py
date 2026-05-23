import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')


def load_data():
    df = pd.read_csv(DATA_PATH)
    # Drop index column if present
    if 'Index' in df.columns:
        df = df.drop(columns=['Index'])
    df = df.drop_duplicates()
    df = df.dropna()
    return df


def prepare_features(df):
    X = df.drop(columns=['class'])
    y = df['class']
    # Map -1 → 0 for binary classification clarity
    y = y.map({-1: 0, 1: 1})
    return X, y


def split_and_scale(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save the scaler
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'scaler.pkl'))
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler



def get_feature_names():
    df = load_data()
    return [c for c in df.columns if c != 'class']