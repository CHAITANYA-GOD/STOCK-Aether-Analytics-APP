import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
try:
    from polygon import RESTClient
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False

import config

ALPHA_VANTAGE_API_KEY = st.secrets.get("ALPHA_VANTAGE_API_KEY")
POLYGON_API_KEY = st.secrets.get("POLYGON_API_KEY")

AV_BASE_URL = 'https://www.alphavantage.co/query'

def map_ticker_for_source(ticker: str, source: str) -> str:
    """
    Map tickers depending on data source.
    - yfinance: NSE stocks need '.NS', US/global stocks stay unchanged.
    - alpha_vantage: expects '.BSE' for Indian stocks, plain for US/global.
    - polygon: same as yfinance, but Indian markets are not fully supported on free tier.
    """
    base = ticker.split('.')[0].upper()
    if source == "yfinance":
        if ticker.endswith('.NSE'):
            return base + ".NS"
        return base
    if source == "alpha_vantage":
        if ticker.endswith('.NSE'):
            return base + ".BSE"
        return base
    if source == "polygon":
        if ticker.endswith('.NSE'):
            st.warning("Polygon.io's free tier has limited support for Indian tickers.")
            return base
        return ticker
    return ticker

def get_period_days(period):
    return {'1mo':30,'3mo':90,'6mo':180,'1y':365,'2y':730,'5y':1825}.get(period,365)

@st.cache_data(ttl=config.CACHE_TTL)
def fetch_stock_data_yfinance(ticker, period="1y"):
    try:
        ticker_mapped = map_ticker_for_source(ticker, "yfinance")
        df = yf.download(
            ticker_mapped,
            period=period,
            interval="1d",
            auto_adjust=True,
            threads=False,
            progress=False
        )
        if df.empty:
            end = datetime.now()
            start = end - timedelta(days=365)
            df = yf.download(
                ticker_mapped,
                start=start.strftime("%Y-%m-%d"),
                end=end.strftime("%Y-%m-%d"),
                interval="1d",
                auto_adjust=True,
                threads=False,
                progress=False
            )
        if df.empty:
            return None
        df.reset_index(inplace=True)
        if "Close" not in df.columns and "Adj Close" in df.columns:
            df["Close"] = df["Adj Close"]
        df.attrs = {'source': 'yfinance'}
        return df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    except Exception:
        return None

@st.cache_data(ttl=config.CACHE_TTL)
def fetch_stock_data_unified(ticker, period="1y"):
    try:
        if not ALPHA_VANTAGE_API_KEY:
            return None
        mapped_ticker = map_ticker_for_source(ticker, "alpha_vantage")
        time.sleep(1)
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': mapped_ticker,
            'apikey': ALPHA_VANTAGE_API_KEY,
            'outputsize': 'full',
            'datatype': 'json'
        }
        response = requests.get(AV_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        if 'Error Message' in data or 'Time Series (Daily)' not in data:
            return None
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index().reset_index().rename(columns={'index': 'Date'})
        days = get_period_days(period)
        start_date = datetime.now() - timedelta(days=days)
        df = df[df['Date'] >= start_date]
        df['Date'] = pd.to_datetime(df['Date'])
        df.attrs = {'source': 'alpha_vantage'}
        return df
    except Exception:
        return None

@st.cache_data(ttl=config.CACHE_TTL)
def fetch_stock_data_polygon(ticker, period="1y"):
    """Fetch stock data from Polygon.io."""
    try:
        if not POLYGON_API_KEY or not POLYGON_AVAILABLE:
            return None
        
        mapped_ticker = map_ticker_for_source(ticker, "polygon")
        days = get_period_days(period)
        end_date_str = datetime.now().strftime('%Y-%m-%d')
        start_date_str = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        client = RESTClient(POLYGON_API_KEY)
        
        resp = client.get_aggs(
            ticker=mapped_ticker,
            multiplier=1,
            timespan="day",
            from_=start_date_str,
            to=end_date_str,
            limit=50000,
        )

        if not resp:
            return None

        data = []
        for agg in resp:
            data.append({
                'Date': datetime.fromtimestamp(agg.timestamp / 1000).strftime('%Y-%m-%d'),
                'Open': agg.open,
                'High': agg.high,
                'Low': agg.low,
                'Close': agg.close,
                'Volume': agg.volume,
            })
        
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df.attrs = {'source': 'polygon'}
        return df
    
    except Exception as e:
        print(f"Error fetching Polygon data: {e}")
        return None

def create_sample_data(ticker, period):
    # Your existing create_sample_data function
    days = get_period_days(period)
    base_prices = {
        'AAPL': 180,'GOOGL': 140,'MSFT': 330,'BLK': 700,'GS': 340,'STT': 70,'TSLA': 250,'AMZN': 140,
        'NVDA': 450,'META': 300,'NFLX': 400,'JPM': 150,'V': 230,'RELIANCE': 2500,'TCS': 3500,
        'PARAS': 700,'INFY': 1500,'HDFCBANK': 1600,'WIPRO': 400,'ITC': 450,'SBIN': 600,
        'TATAMOTORS': 650,'TATASTEEL': 120,'KOTAKBANK': 1900,'BHARTIARTL': 850,'HINDUNILVR': 2500
    }
    base_name = ticker.split('.')[0].upper()
    base_price = base_prices.get(base_name, 1000)
    np.random.seed(hash(ticker) % 2**32)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    daily_return = 0.08 / 252
    volatility = 0.02
    returns = np.random.normal(daily_return, volatility, days)
    prices = [base_price]
    for i in range(1, days):
        new_price = prices[-1] * (1 + returns[i])
        new_price = max(new_price, base_price * 0.5)
        new_price = min(new_price, base_price * 3.0)
        prices.append(new_price)
    data = []
    for i, close_price in enumerate(prices):
        daily_vol = abs(np.random.normal(0, 0.015))
        if i == 0:
            open_price = close_price
        else:
            gap = np.random.normal(0, 0.005)
            open_price = prices[i-1] * (1 + gap)
        intraday_range = abs(np.random.normal(0, daily_vol))
        high = max(open_price, close_price) * (1 + intraday_range)
        low = min(open_price, close_price) * (1 - intraday_range)
        high = max(open_price, close_price, high)
        low = min(open_price, close_price, low)
        base_volume = 1000000 if base_price < 1000 else 100000
        volume = int(np.random.lognormal(np.log(base_volume), 0.8))
        data.append({
            'Date': dates[i],
            'Open': round(open_price, 2),
            'High': round(high, 2),
            'Low': round(low, 2),
            'Close': round(close_price, 2),
            'Volume': volume
        })
    df = pd.DataFrame(data)
    df.attrs = {'source': 'sample_data', 'ticker': ticker}
    return df

def load_stock_data_auto(ticker, period="1y"):
    """
    Try yfinance -> Alpha Vantage -> Polygon.io -> sample, and return (df, used_source, trace_list)
    where trace_list is a list of (source_key, human_message).
    """
    trace = []
    
    # 1) yfinance (preferred free source)
    if YFINANCE_AVAILABLE:
        df_yf = fetch_stock_data_yfinance(ticker, period)
        if df_yf is not None and not df_yf.empty:
            trace.append(("yfinance", "✅ yfinance loaded successfully"))
            return df_yf, "yfinance", trace
        else:
            trace.append(("yfinance", "❌ yfinance failed (no/invalid data)"))
    else:
        trace.append(("yfinance", "❌ yfinance not installed"))
    
    # 2) Alpha Vantage (backup)
    if ALPHA_VANTAGE_API_KEY:
        df_av = fetch_stock_data_unified(ticker, period)
        if df_av is not None and not df_av.empty:
            trace.append(("alpha_vantage", "✅ Alpha Vantage loaded successfully"))
            return df_av, "alpha_vantage", trace
        else:
            trace.append(("alpha_vantage", "❌ Alpha Vantage failed (no/invalid data)"))

    # 3) Polygon.io (only for real-time data, may fail for historical data on free tier)
    if POLYGON_API_KEY and POLYGON_AVAILABLE:
        df_polygon = fetch_stock_data_polygon(ticker, period)
        if df_polygon is not None and not df_polygon.empty:
            trace.append(("polygon", "✅ Polygon.io loaded successfully"))
            return df_polygon, "polygon", trace
        else:
            trace.append(("polygon", "❌ Polygon.io failed (no/invalid data, likely due to plan limitations)"))
    else:
        trace.append(("polygon", "❌ Polygon.io not installed or API key not found"))

    # 4) Sample (last resort)
    df_sample = create_sample_data(ticker, period)
    df_sample.attrs['source'] = 'sample_data'
    trace.append(("sample_data", "⚠️ Using sample data (all APIs unavailable)"))
    return df_sample, "sample_data", trace

def test_api_connections():
    status = {}
    
    # Test yfinance
    if YFINANCE_AVAILABLE:
        try:
            yf.download("AAPL", period="1d", progress=False, threads=False)
            status['yfinance'] = {'working': True, 'message': "✅ yfinance is installed and working."}
        except Exception:
            status['yfinance'] = {'working': False, 'message': "❌ yfinance is installed but failed to fetch data."}
    else:
        status['yfinance'] = {'working': False, 'message': "❌ yfinance library is not installed."}

    # Test Alpha Vantage
    if ALPHA_VANTAGE_API_KEY:
        try:
            response = requests.get(f"{AV_BASE_URL}?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact", timeout=5)
            if response.status_code == 200 and 'Time Series (Daily)' in response.json():
                status['alpha_vantage'] = {'working': True, 'message': "✅ Alpha Vantage API key is valid."}
            else:
                status['alpha_vantage'] = {'working': False, 'message': f"❌ Alpha Vantage API key is invalid or request failed."}
        except Exception as e:
            status['alpha_vantage'] = {'working': False, 'message': f"❌ Alpha Vantage connection failed: {e}"}
    else:
        status['alpha_vantage'] = {'working': False, 'message': "❌ Alpha Vantage API key not found."}
    
    # Test Polygon.io
    if POLYGON_API_KEY and POLYGON_AVAILABLE:
        try:
            client = RESTClient(POLYGON_API_KEY)
            resp = client.get_aggs(ticker="AAPL", multiplier=1, timespan="day", from_="2023-01-09", to="2023-01-09")
            if resp:
                status['polygon'] = {'working': True, 'message': "✅ Polygon.io API key is valid."}
            else:
                status['polygon'] = {'working': False, 'message': "❌ Polygon.io API key is invalid or request failed."}
        except Exception as e:
            status['polygon'] = {'working': False, 'message': f"❌ Polygon.io connection failed: {e}"}
    else:
        status['polygon'] = {'working': False, 'message': "❌ Polygon.io not installed or API key not found."}
        
    return status