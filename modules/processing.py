import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import config
import warnings
warnings.filterwarnings('ignore')

def calculate_rsi(prices, window=14):
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def process_stock_data(df, ticker, source):
    """Process and enhance stock data with technical indicators"""
    if df is None or df.empty:
        return None
    
    if 'Date' not in df.columns and df.index.name == 'Date':
        df = df.reset_index()
    
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df['Close'])
    df['Price_Change'] = df['Close'].pct_change()
    df['Volume_MA'] = df['Volume'].rolling(window=10).mean()
    
    for i in [1, 2, 3, 5]:
        df[f'Close_Lag_{i}'] = df['Close'].shift(i)
    
    df = df.dropna()
    df.attrs = {'source': source,'ticker': ticker,'last_updated': datetime.now()}
    return df

def get_stock_info(ticker):
    stock_info = {
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'industry': 'Consumer Electronics', 'currency': 'USD'},
    'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology', 'industry': 'Software', 'currency': 'USD'},
    'BLK': {'name': 'BlackRock, Inc.', 'sector': 'Financial Services', 'industry': 'Asset Management', 'currency': 'USD'},
    'GS': {'name': 'Goldman Sachs Group, Inc.', 'sector': 'Financial Services', 'industry': 'Capital Markets', 'currency': 'USD'},
    'STT': {'name': 'State Street Corporation', 'sector': 'Financial Services', 'industry': 'Asset Management', 'currency': 'USD'},
    'GOOGL': {'name': 'Alphabet Inc.', 'sector': 'Technology', 'industry': 'Internet Services', 'currency': 'USD'},
    'AMZN': {'name': 'Amazon.com, Inc.', 'sector': 'Consumer Cyclical', 'industry': 'Internet Retail', 'currency': 'USD'},
    'META': {'name': 'Meta Platforms, Inc.', 'sector': 'Communication Services', 'industry': 'Social Media', 'currency': 'USD'},
    'TSLA': {'name': 'Tesla, Inc.', 'sector': 'Consumer Cyclical', 'industry': 'Auto Manufacturers', 'currency': 'USD'},
    'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Technology', 'industry': 'Semiconductors', 'currency': 'USD'},
    'JPM': {'name': 'JPMorgan Chase & Co.', 'sector': 'Financial Services', 'industry': 'Banks—Diversified', 'currency': 'USD'},
    'V': {'name': 'Visa Inc.', 'sector': 'Financial Services', 'industry': 'Credit Services', 'currency': 'USD'},
    'WMT': {'name': 'Walmart Inc.', 'sector': 'Consumer Defensive', 'industry': 'Discount Stores', 'currency': 'USD'},
    'RELIANCE': {'name': 'Reliance Industries Limited', 'sector': 'Energy', 'industry': 'Oil & Gas', 'currency': 'INR'},
    'TCS': {'name': 'Tata Consultancy Services', 'sector': 'Technology', 'industry': 'IT Services', 'currency': 'INR'},
    'PARAS': {'name': 'Paras Defence and Space Technologies Ltd.', 'sector': 'Industrials', 'industry': 'Defense & Aerospace', 'currency': 'INR'},
    'INFY': {'name': 'Infosys Limited', 'sector': 'Technology', 'industry': 'IT Services', 'currency': 'INR'},
    'HDFCBANK': {'name': 'HDFC Bank Limited', 'sector': 'Financial Services', 'industry': 'Banking', 'currency': 'INR'},
    'ICICIBANK': {'name': 'ICICI Bank Limited', 'sector': 'Financial Services', 'industry': 'Banking', 'currency': 'INR'},
    'HINDUNILVR': {'name': 'Hindustan Unilever Limited', 'sector': 'Consumer Defensive', 'industry': 'Household & Personal Products', 'currency': 'INR'},
    'BHARTIARTL': {'name': 'Bharti Airtel Limited', 'sector': 'Communication Services', 'industry': 'Telecom Services', 'currency': 'INR'},
    'SBIN': {'name': 'State Bank of India', 'sector': 'Financial Services', 'industry': 'Banking', 'currency': 'INR'},
    'ITC': {'name': 'ITC Limited', 'sector': 'Consumer Defensive', 'industry': 'Tobacco & FMCG', 'currency': 'INR'},
    'KOTAKBANK': {'name': 'Kotak Mahindra Bank Limited', 'sector': 'Financial Services', 'industry': 'Banking', 'currency': 'INR'},
    }
    
    base_ticker = ticker.split('.')[0].upper()
    info = stock_info.get(base_ticker, {
        'name': ticker,'sector': 'Unknown','industry': 'Unknown','currency': 'USD'
    })
    info['market_cap'] = 'N/A'
    return info

def safe_stat(df, col, func, label, fmt="{:.2f}", currency_symbol=""):
    try:
        if df is not None and col in df.columns and not df[col].dropna().empty:
            val = func(df[col].dropna())
            if pd.notna(val):
                st.write(f"- {label}: {currency_symbol}{fmt.format(val)}")
                return
    except Exception:
        pass
    st.write(f"- {label}: Data not available")