import streamlit as st

# Caching TTL in seconds
CACHE_TTL = 300

# API Keys (You should store these in st.secrets)
# ALPHA_VANTAGE_API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]
# FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"] # Placeholder for your Finnhub key

# Enhanced stock tickers
RELIABLE_TICKERS = {
    "US Markets": {
        "AAPL": "Apple Inc.",
        "GOOGL": "Alphabet Inc.",
        "MSFT": "Microsoft Corporation",
        "BLK": "BlackRock Inc.",
        "GS": "Goldman Sachs Group Inc.",
        "STT": "State Street Corporation",
        "TSLA": "Tesla Inc.",
        "AMZN": "Amazon.com Inc.",
        "NVDA": "NVIDIA Corporation",
        "META": "Meta Platforms Inc.",
        "NFLX": "Netflix Inc.",
        "JPM": "JPMorgan Chase & Co.",
        "V": "Visa Inc."
    },
    "Indian Markets": {
        "RELIANCE.NSE": "Reliance Industries",
        "TCS.NSE": "Tata Consultancy Services",
        "PARAS.NSE": "Paras Defence and Space Technologies",
        "INFY.NSE": "Infosys Limited",
        "HDFCBANK.NSE": "HDFC Bank",
        "WIPRO.NSE": "Wipro Limited",
        "ITC.NSE": "ITC Limited",
        "SBIN.NSE": "State Bank of India",
        "TATAMOTORS.NSE": "Tata Motors",
        "TATASTEEL.NSE": "Tata Steel",
        "KOTAKBANK.NSE": "Kotak Mahindra Bank",
        "BHARTIARTL.NSE": "Bharti Airtel",
        "HINDUNILVR.NSE": "Hindustan Unilever",
        "BAJFINANCE.NSE": "Bajaj Finance Limited", 
        "HCLTECH.NSE": "HCL Technologies Limited", 
        "AXISBANK.NSE": "Axis Bank Limited",      # 3
        "ASIANPAINT.NSE": "Asian Paints Limited", # 4
        "WIPRO.NSE": "Wipro Limited",            # 5
        "SUNPHARMA.NSE": "Sun Pharmaceutical Ind.",# 6
        "TITAN.NSE": "Titan Company Limited",    # 7
        "NESTLEIND.NSE": "Nestle India Limited", # 8
        "MARUTI.NSE": "Maruti Suzuki India Ltd.", # 9
        "GRASIM.NSE": "Grasim Industries Limited" # 10
    }
}