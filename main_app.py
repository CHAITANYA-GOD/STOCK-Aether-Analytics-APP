'''import streamlit as st
import pandas as pd
import numpy as np
from modules import data_fetcher, processing, model, charting, ui
import warnings
warnings.filterwarnings('ignore')

# --- Page configuration ---
st.set_page_config(
    page_title="Aether Analytics",
    page_icon="brain.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Apply custom CSS ---
ui.apply_css()

def main():
    ui.display_header()

    # --- API Status Check Expander ---
    with st.expander("🔍 API Status Check", expanded=False):
        if st.button("🔄 Test API Connections", type="primary"):
            with st.spinner("Testing API connections..."):
                api_status = data_fetcher.test_api_connections()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 yfinance Status")
                css_class = "api-working" if api_status['yfinance']['working'] else "api-failed"
                st.markdown(f'<div class="api-status {css_class}">{api_status["yfinance"]["message"]}</div>', unsafe_allow_html=True)
            with col2:
                st.subheader("🔑 Alpha Vantage Status")
                css_class = "api-working" if api_status['alpha_vantage']['working'] else "api-failed"
                st.markdown(f'<div class="api-status {css_class}">{api_status["alpha_vantage"]["message"]}</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        ui.display_sidebar_header()
        data_source_choice, ticker, period, prediction_days, predict_button = ui.get_user_inputs()

    if predict_button:
        if not ticker:
            st.error("Please enter a stock ticker symbol!")
            return

        with st.spinner(f"🔄 Fetching data for {ticker}..."):
            if data_source_choice == "Auto (yfinance → Alpha Vantage → Sample)":
                df, used_source, trace = data_fetcher.load_stock_data_auto(ticker, period)
                ui.display_api_status(trace)
            elif data_source_choice == "yfinance":
                df = data_fetcher.fetch_stock_data_yfinance(ticker, period)
                used_source = "yfinance" if df is not None else None
            elif data_source_choice == "Alpha Vantage":
                df = data_fetcher.fetch_stock_data_unified(ticker, period)
                used_source = "alpha_vantage" if df is not None else None

            if df is None or df.empty:
                st.error("❌ Unable to fetch real data. Using sample data.")
                df = data_fetcher.create_sample_data(ticker, period)
                used_source = "sample_data"

        # Process the data and get info
        df = processing.process_stock_data(df, ticker, used_source)
        stock_info = processing.get_stock_info(ticker)
        currency_symbol = '$' if stock_info.get('currency', 'USD') == 'USD' else '₹'

        if df is None or df.empty:
            st.error("❌ Unable to process stock data. Please try again.")
            return

        st.success(f"✅ Successfully loaded {len(df)} data points for {ticker} from {used_source}")
        
        current_price_val = float(df['Close'].iloc[-1]) if 'Close' in df.columns and not df.empty else None
        price_change = float(df['Close'].iloc[-1]) - float(df['Close'].iloc[-2]) if len(df) > 1 else 0.0
        pct_change = (price_change / float(df['Close'].iloc[-2])) * 100 if len(df) > 1 and float(df['Close'].iloc[-2]) != 0 else 0.0
        volume = int(float(df['Volume'].iloc[-1])) if 'Volume' in df.columns and len(df) > 0 else None
        
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std() * (252 ** 0.5) if len(returns) > 2 else None
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Stock Analysis", "🔮 Predictions", "📈 Charts", 
            "🤖 Model Performance", "📋 Data Table"
        ])
        
        with tab1:
            ui.display_stock_analysis(df, ticker, stock_info, currency_symbol, current_price_val, price_change, pct_change, volume, volatility)

        with tab2:
            with st.spinner("🧠 Training ML model..."):
                trained_model, scaler, metrics, feature_importance = model.train_model(df)
            
            if trained_model:
                ui.display_prediction_metrics(metrics)
                next_day_pred = model.predict_next_price(trained_model, scaler, df)
                ui.display_next_day_prediction(next_day_pred, df, currency_symbol)
            else:
                st.error("Failed to train model due to insufficient data or error.")

        with tab3:
            charting.display_charts(df, ticker, currency_symbol)
            
        with tab4:
            # Crucial fix: Check if the model was trained successfully before calling the display function
            if trained_model:
                ui.display_model_performance(metrics, feature_importance)
            else:
                st.warning("⚠️ No model performance data available. Training failed.")
            
        with tab5:
            ui.display_data_table(df, ticker)
            
        ui.display_disclaimer()
    else:
        ui.display_welcome_screen()

if __name__ == "__main__":
    main()'''



# main.py
import streamlit as st
import pandas as pd
import numpy as np
from modules import data_fetcher, processing, model, charting, ui
import warnings
warnings.filterwarnings('ignore')

# --- Page configuration ---
st.set_page_config(
    page_title="Aether Analytics",
    page_icon="brain.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # --- Apply custom CSS from file ---
    ui.apply_css_from_file("style.css")
    
    # --- Main Header and API Status Check ---
    ui.display_header()
    with st.expander("🔍 API Status Check", expanded=False):
        if st.button("🔄 Test API Connections", type="primary"):
            with st.spinner("Testing API connections..."):
                api_status = data_fetcher.test_api_connections()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 yfinance Status")
                css_class = "api-working" if api_status['yfinance']['working'] else "api-failed"
                st.markdown(f'<div class="api-status {css_class}">{api_status["yfinance"]["message"]}</div>', unsafe_allow_html=True)
            with col2:
                st.subheader("🔑 Alpha Vantage Status")
                css_class = "api-working" if api_status['alpha_vantage']['working'] else "api-failed"
                st.markdown(f'<div class="api-status {css_class}">{api_status["alpha_vantage"]["message"]}</div>', unsafe_allow_html=True)
    
    # --- Sidebar for User Inputs ---
    with st.sidebar:
        ui.display_sidebar_header()
        data_source_choice, ticker, period, prediction_days, predict_button = ui.get_user_inputs()

    if predict_button:
        if not ticker:
            st.error("Please enter a stock ticker symbol!")
            return

        with st.spinner(f"🔄 Fetching data for {ticker}..."):
            # The corrected line: Unpack 3 values
            df, used_source, trace = data_fetcher.load_stock_data_auto(ticker, period)
            ui.display_api_status(trace) # Re-add this line

            if df is None or df.empty:
                st.error("❌ Unable to fetch real data. Using sample data.")
                df = data_fetcher.create_sample_data(ticker, period)
                used_source = "sample_data"

        # Process the data and get info
        df = processing.process_stock_data(df, ticker, used_source)
        stock_info = processing.get_stock_info(ticker)
        currency_symbol = '$' if stock_info.get('currency', 'USD') == 'USD' else '₹'

        if df is None or df.empty:
            st.error("❌ Unable to process stock data. Please try again.")
            return

        st.success(f"✅ Successfully loaded {len(df)} data points for {ticker} from {used_source}")
        
        current_price_val = float(df['Close'].iloc[-1]) if 'Close' in df.columns and not df.empty else None
        price_change = float(df['Close'].iloc[-1]) - float(df['Close'].iloc[-2]) if len(df) > 1 else 0.0
        pct_change = (price_change / float(df['Close'].iloc[-2])) * 100 if len(df) > 1 and float(df['Close'].iloc[-2]) != 0 else 0.0
        volume = int(float(df['Volume'].iloc[-1])) if 'Volume' in df.columns and len(df) > 0 else None
        
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std() * (252 ** 0.5) if len(returns) > 2 else None
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Stock Analysis", "🔮 Predictions", "📈 Charts", 
            "🤖 Model Performance", "📋 Data Table"
        ])
        
        with tab1:
            ui.display_stock_analysis(df, ticker, stock_info, currency_symbol, current_price_val, price_change, pct_change, volume, volatility)

        with tab2:
            with st.spinner("🧠 Training ML model..."):
                trained_model, scaler, metrics, feature_importance = model.train_model(df)
            
            if trained_model:
                ui.display_prediction_metrics(metrics)
                next_day_pred = model.predict_next_price(trained_model, scaler, df)
                ui.display_next_day_prediction(next_day_pred, df, currency_symbol)
            else:
                st.error("Failed to train model due to insufficient data or an error.")

        with tab3:
            charting.display_charts(df, ticker, currency_symbol)
            
        with tab4:
            if trained_model:
                ui.display_model_performance(metrics, feature_importance)
            else:
                st.warning("⚠️ No model performance data available. Training failed.")
            
        with tab5:
            ui.display_data_table(df, ticker)
            
        ui.display_disclaimer()
    else:
        ui.display_welcome_screen()

if __name__ == "__main__":
    main()

