import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def prepare_features(df):
    feature_columns = ['Open', 'High', 'Low', 'Volume', 'MA_20', 'MA_50', 'RSI','Price_Change', 'Volume_MA']
    for i in [1, 2, 3, 5]:
        if f'Close_Lag_{i}' in df.columns:
            feature_columns.append(f'Close_Lag_{i}')
    existing_features = [col for col in feature_columns if col in df.columns]
    X = df[existing_features].copy()
    y = df['Close'].copy()
    return X, y, existing_features

def train_model(df):
    try:
        X, y, feature_names = prepare_features(df)
        if X.empty or y.empty:
            st.error("Insufficient data for training")
            return None, None, None, None
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        y_train_pred = model.predict(X_train_scaled)
        y_test_pred = model.predict(X_test_scaled)
        metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'test_mae': mean_absolute_error(y_test, y_test_pred),
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        return model, scaler, metrics, feature_importance
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return None, None, None, None

def predict_next_price(model, scaler, df):
    try:
        X, _, feature_names = prepare_features(df)
        if X.empty:
            return None
        last_features = X.iloc[-1:].values
        last_features_scaled = scaler.transform(last_features)
        prediction = model.predict(last_features_scaled)[0]
        return prediction
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None