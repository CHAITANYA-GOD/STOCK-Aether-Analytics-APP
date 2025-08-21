'''import streamlit as st
import pandas as pd
from datetime import datetime
from modules import processing
import config
import plotly.express as px

def apply_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            .main-header {font-size: 3.5rem;font-weight: 700;background: linear-gradient(45deg, #1f77b4, #ff7f0e);-webkit-background-clip: text;-webkit-text-fill-color: transparent;background-clip: text;text-align: center;margin-bottom: 1rem;font-family: 'Inter', sans-serif;}
            .subtitle {text-align: center;font-size: 1.3rem;color: #666;margin-bottom: 3rem;font-weight: 300;}
            .warning-card {background: #000000;padding: 1.5rem;border-radius: 8px;border: 1px solid #ffeaa7;margin-top: 2rem;border-left: 4px solid #fdcb6e;}
            .api-status {padding: 1rem;border-radius: 8px;margin: 1rem 0;}
            .api-working {background: #d4edda;color: #155724;border: 1px solid #c3e6cb;}
            .api-failed {background: #f8d7da;color: #721c24;border: 1px solid #f5c6cb;}
            .stButton > button {background: linear-gradient(45deg, #1f77b4, #ff7f0e);color: white;border: none;padding: 0.75rem 1.5rem;border-radius: 8px;font-weight: 600;font-size: 1rem;transition: all 0.3s ease;width: 100%;}
            .stButton > button:hover {background: linear-gradient(45deg, #1565c0, #f57c00);transform: translateY(-2px);box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);}
            #MainMenu {visibility: visible;}
            footer {visibility: visible;}
            header {visibility: visible;}
            section[data-testid="stSidebar"] {background: #f9f9f9 !important;color: #000000 !important;--background-color:#f9f9f9;--secondary-background-color:#ffffff;--text-color:#000000;--font-color:#000000;--border-color:#DDDDDD;}
        </style>
    """, unsafe_allow_html=True)

def display_header():
    st.markdown('<h1 class="main-header">Aether Analytics</h1>', unsafe_allow_html=True)
    st.markdown(
    """
    <p style='text-align: center;font-size: 20px;font-weight: 500;background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe);-webkit-background-clip: text;-webkit-text-fill-color: transparent;margin-top: -10px;margin-bottom: 20px;'>
        Advanced Market Analysis & AI-Powered Prediction Platform
    </p>
    """,
    unsafe_allow_html=True
    )

def display_sidebar_header():
    st.markdown("### ⚙️ Configuration")
    st.markdown(
        """
        <style>
        .api-badge {background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);color: white;padding: 8px 18px;border-radius: 25px;font-size: 15px;font-weight: 600;display: inline-block;box-shadow: 0px 4px 10px rgba(0,0,0,0.2);animation: pulse 2s infinite;}
        @keyframes pulse {0% { box-shadow: 0 0 0 0 rgba(79,172,254,0.6); }70% { box-shadow: 0 0 0 12px rgba(79,172,254,0); }100% { box-shadow: 0 0 0 0 rgba(79,172,254,0); }}
        </style>
        <div class="api-badge">💎 Premium API Access Enabled</div>
        """,
        unsafe_allow_html=True
    )

def get_user_inputs():
    st.markdown("#### 📡 Data Source")
    data_source_choice = st.selectbox(
        "Select Data Source",
        ["yfinance", "Alpha Vantage", "Auto (yfinance → Alpha Vantage → Sample)"],
        index=0,
        help="Choose the data source. 'Auto' tries yfinance first, then Alpha Vantage, then sample data."
    )
    
    st.markdown("#### 📈 Stock Selection")
    market = st.selectbox(
        "Select Market",
        ["US Markets", "Indian Markets", "Custom Ticker"],
        help="Choose your preferred market or enter a custom ticker"
    )

    if market != "Custom Ticker":
        stock_options = config.RELIABLE_TICKERS[market]
        selected_stock = st.selectbox("Select Stock", list(stock_options.keys()))
        ticker = selected_stock
        st.info(f"📊 Selected: {stock_options[selected_stock]}")
    else:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="Examples: AAPL (US), RELIANCE.NSE (Indian stocks with .NSE extension)"
        )
        if ticker:
            if ticker.endswith('.NSE'):
                st.info("🇮🇳 Indian stock format detected")
            else:
                st.info("🇺🇸 US stock format detected")

    st.markdown("#### 📅 Time Period")
    period = st.selectbox(
        "Select Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        help="Choose the historical data period for analysis"
    )

    st.markdown("#### 🔮 Prediction Settings")
    prediction_days = st.slider("Days to Predict", 1, 30, 7, help="Number of days to predict into the future")
    predict_button = st.button("🚀 Predict Stock Price", type="primary", use_container_width=True)

    return data_source_choice, ticker, period, prediction_days, predict_button

def display_api_status(trace):
    st.markdown("#### 🔎 API Call Status")
    for src, msg in trace:
        css_class = "api-working" if "✅" in msg else "api-failed"
        st.markdown(f'<div class="api-status {css_class}">{msg}</div>', unsafe_allow_html=True)

def display_stock_analysis(df, ticker, stock_info, currency_symbol, current_price_val, price_change, pct_change, volume, volatility):
    st.markdown(f"### 📋 {stock_info['name']} ({ticker})")
    data_source = df.attrs.get('source')
    if data_source != 'sample_data':
        st.info(f"📡 Data Source: {data_source.title()}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"{currency_symbol}{float(current_price_val):.2f}" if current_price_val is not None else "Data not available")
    with col2:
        st.metric("Price Change", f"{currency_symbol}{price_change:.2f}", f"{pct_change:.2f}%")
    with col3:
        st.metric("Volume", f"{volume:,.0f}" if volume is not None else "Data not available")
    with col4:
        # Corrected: Check if volatility is a valid number before formatting
        if isinstance(volatility, (float, int)) and not pd.isna(volatility):
            st.metric("Volatility (annualized %)", f"{volatility*100:.2f}%")
        else:
            st.metric("Volatility", "Data not available")
    st.markdown("### 📊 Stock Details")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Sector:** {stock_info['sector']}")
        st.write(f"**Industry:** {stock_info['industry']}")
    with col2:
        st.write(f"**Market Cap:** {stock_info['market_cap']}")
        st.write(f"**Currency:** {stock_info['currency']}")
    st.markdown("### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_52w = float(df['High'].max()) if not df.empty and 'High' in df.columns else None
        st.metric("52W High", f"{currency_symbol}{high_52w:.2f}" if high_52w is not None else "Data not available")
    with col2:
        low_52w = float(df['Low'].min()) if not df.empty and 'Low' in df.columns else None
        st.metric("52W Low", f"{currency_symbol}{low_52w:.2f}" if low_52w is not None else "Data not available")
    with col3:
        avg_volume_val = float(df['Volume'].mean()) if not df.empty and 'Volume' in df.columns else None
        st.metric("Avg Volume", f"{avg_volume_val:,.0f}" if avg_volume_val is not None else "Data not available")
    with col4:
        current_rsi = df['RSI'].iloc[-1] if 'RSI' in df.columns and not df['RSI'].isna().all() else None
        st.metric("RSI", f"{current_rsi:.1f}" if current_rsi is not None else "Data not available")

def display_prediction_metrics(metrics):
    st.markdown("### 🤖 AI Predictions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy (R²)", f"{metrics['test_r2']:.3f}")
    with col2:
        st.metric("RMSE", f"{metrics['test_rmse']:.2f}")
    with col3:
        st.metric("MAE", f"{metrics['test_mae']:.2f}")

def display_next_day_prediction(prediction, df, currency_symbol):
    st.markdown("### 🔮 Next Day Prediction")
    if prediction is not None:
        try:
            current_price_num = float(df['Close'].iloc[-1])
            price_change = float(prediction) - current_price_num
            percentage_change = (price_change / current_price_num) * 100 if current_price_num != 0 else 0.0
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"{currency_symbol}{current_price_num:.2f}")
            with col2:
                st.metric("Predicted Price", f"{currency_symbol}{float(prediction):.2f}", f"{currency_symbol}{price_change:.2f}")
            with col3:
                st.metric("Expected Change", f"{percentage_change:.2f}%")
            if percentage_change > 2:
                st.success("🟢 Strong Bullish Signal")
            elif percentage_change > 0:
                st.info("🔵 Mild Bullish Signal")
            elif percentage_change > -2:
                st.warning("🟡 Neutral Signal")
            else:
                st.error("🔴 Bearish Signal")
        except Exception:
            st.error("Could not display prediction metrics.")

def display_model_performance(metrics, feature_importance):
    if metrics is not None:
        st.markdown("### 🤖 Model Performance Details")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Training Metrics:**")
            st.write(f"- RMSE: {metrics['train_rmse']:.4f}")
            st.write(f"- MAE: {metrics['train_mae']:.4f}")
            st.write(f"- R² Score: {metrics['train_r2']:.4f}")
            st.write(f"- Sample Size: {metrics['train_size']}")
        with col2:
            st.markdown("**📊 Testing Metrics:**")
            st.write(f"- RMSE: {metrics['test_rmse']:.4f}")
            st.write(f"- MAE: {metrics['test_mae']:.4f}")
            st.write(f"- R² Score: {metrics['test_r2']:.4f}")
            st.write(f"- Sample Size: {metrics['test_size']}")
        st.markdown("### 🎯 Model Interpretation")
        if metrics['test_r2'] > 0.8:
            st.success("🎯 Excellent model performance! High accuracy predictions.")
        elif metrics['test_r2'] > 0.6:
            st.info("👍 Good model performance. Reliable predictions.")
        elif metrics['test_r2'] > 0.4:
            st.warning("⚠️ Moderate model performance. Use predictions with caution.")
        else:
            st.error("❌ Poor model performance. Predictions may be unreliable.")
        if feature_importance is not None and not feature_importance.empty:
            st.markdown("### 🎯 Feature Importance")
            fig_importance = px.bar(
                feature_importance.head(10), x='importance', y='feature', orientation='h',
                title="Top 10 Most Important Features", color='importance', color_continuous_scale='viridis',
                template='plotly_white'
            )
            fig_importance.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_importance, use_container_width=True)
            st.info("""**📋 Feature Importance Explanation:**
            - **Close_Lag_X**: Previous day closing prices
            - **MA_X**: Moving averages (trend indicators)
            - **RSI**: Relative Strength Index (momentum indicator)
            - **Volume**: Trading volume
            - **Price_Change**: Recent price change percentage
            """)

def display_data_table(df, ticker):
    st.markdown("### 📋 Historical Data")
    display_df = df.tail(50).copy()
    if 'Date' in display_df.columns:
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    if 'MA_20' in display_df.columns:
        display_columns.append('MA_20')
    if 'RSI' in display_df.columns:
        display_columns.append('RSI')
    display_df = display_df[display_columns]
    st.dataframe(display_df, use_container_width=True)
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"{ticker}_stock_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        type="primary"
    )

def display_disclaimer():
    st.markdown("""
    <div class="warning-card">
        <strong>⚠️ Important Disclaimer:</strong><br>
        This application is designed for educational and research purposes only. 
        Stock price predictions are inherently uncertain and should never be used as the sole basis for investment decisions. 
        <br><br>
        <strong>🔍 Please Note:</strong>
        <ul>
            <li>Past performance does not guarantee future results</li>
            <li>Market conditions can change rapidly and unpredictably</li>
            <li>Always consult with qualified financial advisors</li>
            <li>Conduct your own thorough research before making investment decisions</li>
            <li>Only invest what you can afford to lose</li>
        </ul>
        <br>
        <strong>📊 Data Sources:</strong> This application utilizes multiple data sources including Alpha Vantage API 
        and may fall back to sample data for demonstration when live APIs is unavailable.
    </div>
    """, unsafe_allow_html=True)

def display_welcome_screen():
    st.markdown(
        """
        <h2 style='text-align: center;font-size: 40px;font-weight: 800;background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe);-webkit-background-clip: text;-webkit-text-fill-color: transparent;text-decoration: none;margin-bottom: 20px;'>
            🧠 Cortex-o1 Predictive Model
        </h2>
        """,
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            ### ✨ Premium Features:
            - 🔄 **Multi-API Integration**: Seamless data fetching from Alpha Vantage & yfinance
            - 🤖 **Advanced AI Models**: Machine learning-powered predictions
            - 📊 **Comprehensive Analysis**: Technical indicators & market insights
            - 🎨 **Premium Interface**: Beautiful, responsive dark theme
            - 📈 **Real-time Charts**: Interactive Plotly visualizations
            - 🔍 **Performance Metrics**: Detailed model evaluation & statistics
            ### 🌍 Global Market Coverage:
            **🇺🇸 US Stocks:**
            - Apple (AAPL), Microsoft (MSFT), Alphabet/Google (GOOGL)
            - Amazon (AMZN), Tesla (TSLA), NVIDIA (NVDA)
            - Meta (META), Netflix (NFLX)
            - JPMorgan (JPM), Visa (V)
            - BlackRock (BLK), Goldman Sachs (GS), State Street (STT)
            **🇮🇳 Indian Stocks:**
            - Reliance (RELIANCE.NSE), TCS (TCS.NSE), Infosys (INFY.NSE)
            - HDFC Bank (HDFCBANK.NSE), Wipro (WIPRO.NSE), ITC (ITC.NSE)
            - SBI (SBIN.NSE), Kotak Bank (KOTAKBANK.NSE), Bharti Airtel (BHARTIARTL.NSE)
            - Hindustan Unilever (HINDUNILVR.NSE), Tata Motors (TATAMOTORS.NSE)
            - Tata Steel (TATASTEEL.NSE), Paras Defence (PARAS.NSE)
            """)
    with col2:
        st.markdown("""
            ### 🎯 How It Works:
            1. 📊 **Select Your Stock**: Pick from curated tickers or enter a custom symbol  
            2. ⏱️ **Choose Time Period**: Analyze 1 month → 5 years of data  
            3. 🤖 **AI Analysis**: ML models learn market patterns  
            4. 🔮 **Get Predictions**: Forecast next-day/multi-day prices with confidence  
            5. 📈 **Visualize Results**: Interactive charts & detailed analytics
            ### 🛠️ Technical Features:
            - 🧠 **Machine Learning**: Random Forest, Feature Engineering  
            - 🔁 **Cross-validation**: Performance metrics built-in  
            - 📊 **Technical Indicators**: Moving Averages (20/50d), RSI, Volume Analysis  
            - 📈 **Visualizations**: Interactive Price & Volume charts, RSI Momentum, Feature Importance  
            ### 💡 Pro Tips:
            - 📅 Use longer timeframes (1y+) for more reliable predictions  
            - 🌍 Consider external market/economic context  
            - ⏳ Compare predictions across different timeframes  
            - 🛡️ Always diversify your portfolio  
            """)
    st.markdown(
        """
        ---
        👈 Use the **sidebar** to configure your settings and begin exploring the power of **AI-driven stock prediction!**
        """,
        unsafe_allow_html=True
    )'''




import streamlit as st
import pandas as pd
from datetime import datetime
from modules import processing
import config
import plotly.express as px
import os

# 1. Add this line to set the browser tab title
st.set_page_config(page_title="Aether Analytics")

def apply_css_from_file(css_file):
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {css_file}")

def display_header():
    # 3. Added the lightning bolt emoji
    st.markdown('<h1 class="main-header">⚡ Aether Analytics</h1>', unsafe_allow_html=True)
    st.markdown(
    """
    <p style='text-align: center;font-size: 20px;font-weight: 500;background: -webkit-linear-gradient(45deg, #00aaff, #ff00c8);-webkit-background-clip: text;-webkit-text-fill-color: transparent;margin-top: -10px;margin-bottom: 20px; text-shadow: 0 0 5px #00aaff;'>
        Advanced Market Analysis & AI-Powered Prediction Platform
    </p>
    """,
    unsafe_allow_html=True
    )

def display_sidebar_header():
    st.markdown("### ⚙️ Configuration")
    st.markdown(
        """
        <div class="api-badge">💎 Premium API Access Enabled</div>
        """,
        unsafe_allow_html=True
    )

def get_user_inputs():
    st.markdown("#### 📡 Data Source")
    data_source_choice = st.selectbox(
        "Select Data Source",
        ["yfinance", "Alpha Vantage", "Auto (yfinance → Alpha Vantage → Sample)"],
        index=0,
        help="Choose the data source. 'Auto' tries yfinance first, then Alpha Vantage, then sample data."
    )
    
    st.markdown("#### 📈 Stock Selection")
    market = st.selectbox(
        "Select Market",
        ["US Markets", "Indian Markets", "Custom Ticker"],
        help="Choose your preferred market or enter a custom ticker"
    )

    if market != "Custom Ticker":
        stock_options = config.RELIABLE_TICKERS[market]
        selected_stock = st.selectbox("Select Stock", list(stock_options.keys()))
        ticker = selected_stock
        st.info(f"📊 Selected: {stock_options[selected_stock]}")
    else:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="Examples: AAPL (US), RELIANCE.NSE (Indian stocks with .NSE extension)"
        )
        if ticker:
            if ticker.endswith('.NSE'):
                st.info("🇮🇳 Indian stock format detected")
            else:
                st.info("🇺🇸 US stock format detected")

    st.markdown("#### 📅 Time Period")
    period = st.selectbox(
        "Select Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        help="Choose the historical data period for analysis"
    )

    st.markdown("#### 🔮 Prediction Settings")
    prediction_days = st.slider("Days to Predict", 1, 30, 7, help="Number of days to predict into the future")
    predict_button = st.button("🚀 Predict Stock Price", type="primary", use_container_width=True)

    return data_source_choice, ticker, period, prediction_days, predict_button

def display_api_status(trace):
    st.markdown("#### 🔎 API Call Status")
    for src, msg in trace:
        css_class = "api-working" if "✅" in msg else "api-failed"
        st.markdown(f'<div class="api-status {css_class}">{msg}</div>', unsafe_allow_html=True)

def display_stock_analysis(df, ticker, stock_info, currency_symbol, current_price_val, price_change, pct_change, volume, volatility):
    st.markdown(f"### 📋 {stock_info['name']} ({ticker})")
    data_source = df.attrs.get('source')
    if data_source != 'sample_data':
        st.info(f"📡 Data Source: {data_source.title()}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"{currency_symbol}{float(current_price_val):.2f}" if current_price_val is not None else "Data not available")
    with col2:
        st.metric("Price Change", f"{currency_symbol}{price_change:.2f}", f"{pct_change:.2f}%")
    with col3:
        st.metric("Volume", f"{volume:,.0f}" if volume is not None else "Data not available")
    with col4:
        # Corrected: Check if volatility is a valid number before formatting
        if isinstance(volatility, (float, int)) and not pd.isna(volatility):
            st.metric("Volatility (annualized %)", f"{volatility*100:.2f}%")
        else:
            st.metric("Volatility", "Data not available")
    st.markdown("### 📊 Stock Details")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Sector:** {stock_info['sector']}")
        st.write(f"**Industry:** {stock_info['industry']}")
    with col2:
        st.write(f"**Market Cap:** {stock_info['market_cap']}")
        st.write(f"**Currency:** {stock_info['currency']}")
    st.markdown("### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_52w = float(df['High'].max()) if not df.empty and 'High' in df.columns else None
        st.metric("52W High", f"{currency_symbol}{high_52w:.2f}" if high_52w is not None else "Data not available")
    with col2:
        low_52w = float(df['Low'].min()) if not df.empty and 'Low' in df.columns else None
        st.metric("52W Low", f"{currency_symbol}{low_52w:.2f}" if low_52w is not None else "Data not available")
    with col3:
        avg_volume_val = float(df['Volume'].mean()) if not df.empty and 'Volume' in df.columns else None
        st.metric("Avg Volume", f"{avg_volume_val:,.0f}" if avg_volume_val is not None else "Data not available")
    with col4:
        current_rsi = df['RSI'].iloc[-1] if 'RSI' in df.columns and not df['RSI'].isna().all() else None
        st.metric("RSI", f"{current_rsi:.1f}" if current_rsi is not None else "Data not available")

def display_prediction_metrics(metrics):
    st.markdown("### 🤖 AI Predictions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy (R²)", f"{metrics['test_r2']:.3f}")
    with col2:
        st.metric("RMSE", f"{metrics['test_rmse']:.2f}")
    with col3:
        st.metric("MAE", f"{metrics['test_mae']:.2f}")

def display_next_day_prediction(prediction, df, currency_symbol):
    st.markdown("### 🔮 Next Day Prediction")
    if prediction is not None:
        try:
            current_price_num = float(df['Close'].iloc[-1])
            price_change = float(prediction) - current_price_num
            percentage_change = (price_change / current_price_num) * 100 if current_price_num != 0 else 0.0
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"{currency_symbol}{current_price_num:.2f}")
            with col2:
                st.metric("Predicted Price", f"{currency_symbol}{float(prediction):.2f}", f"{currency_symbol}{price_change:.2f}")
            with col3:
                st.metric("Expected Change", f"{percentage_change:.2f}%")
            if percentage_change > 2:
                st.success("🟢 Strong Bullish Signal")
            elif percentage_change > 0:
                st.info("🔵 Mild Bullish Signal")
            elif percentage_change > -2:
                st.warning("🟡 Neutral Signal")
            else:
                st.error("🔴 Bearish Signal")
        except Exception:
            st.error("Could not display prediction metrics.")

def display_model_performance(metrics, feature_importance):
    if metrics is not None:
        st.markdown("### 🤖 Model Performance Details")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Training Metrics:**")
            st.write(f"- RMSE: {metrics['train_rmse']:.4f}")
            st.write(f"- MAE: {metrics['train_mae']:.4f}")
            st.write(f"- R² Score: {metrics['train_r2']:.4f}")
            st.write(f"- Sample Size: {metrics['train_size']}")
        with col2:
            st.markdown("**📊 Testing Metrics:**")
            st.write(f"- RMSE: {metrics['test_rmse']:.4f}")
            st.write(f"- MAE: {metrics['test_mae']:.4f}")
            st.write(f"- R² Score: {metrics['test_r2']:.4f}")
            st.write(f"- Sample Size: {metrics['test_size']}")
        st.markdown("### 🎯 Model Interpretation")
        if metrics['test_r2'] > 0.8:
            st.success("🎯 Excellent model performance! High accuracy predictions.")
        elif metrics['test_r2'] > 0.6:
            st.info("👍 Good model performance. Reliable predictions.")
        elif metrics['test_r2'] > 0.4:
            st.warning("⚠️ Moderate model performance. Use predictions with caution.")
        else:
            st.error("❌ Poor model performance. Predictions may be unreliable.")
        if feature_importance is not None and not feature_importance.empty:
            st.markdown("### 🎯 Feature Importance")
            fig_importance = px.bar(
                feature_importance.head(10), x='importance', y='feature', orientation='h',
                title="Top 10 Most Important Features", color='importance', color_continuous_scale='viridis',
                template='plotly_white'
            )
            fig_importance.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_importance, use_container_width=True)
            st.info("""**📋 Feature Importance Explanation:**
            - **Close_Lag_X**: Previous day closing prices
            - **MA_X**: Moving averages (trend indicators)
            - **RSI**: Relative Strength Index (momentum indicator)
            - **Volume**: Trading volume
            - **Price_Change**: Recent price change percentage
            """)

def display_data_table(df, ticker):
    st.markdown("### 📋 Historical Data")
    display_df = df.tail(50).copy()
    if 'Date' in display_df.columns:
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    if 'MA_20' in display_df.columns:
        display_columns.append('MA_20')
    if 'RSI' in display_df.columns:
        display_columns.append('RSI')
    display_df = display_df[display_columns]
    st.dataframe(display_df, use_container_width=True)
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"{ticker}_stock_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        type="primary"
    )

def display_disclaimer():
    st.markdown("""
    <div class="warning-card">
        <strong>⚠️ Important Disclaimer:</strong><br>
        This application is designed for educational and research purposes only. 
        Stock price predictions are inherently uncertain and should never be used as the sole basis for investment decisions. 
        <br><br>
        <strong>🔍 Please Note:</strong>
        <ul>
            <li>Past performance does not guarantee future results</li>
            <li>Market conditions can change rapidly and unpredictably</li>
            <li>Always consult with qualified financial advisors</li>
            <li>Conduct your own thorough research before making investment decisions</li>
            <li>Only invest what you can afford to lose</li>
        </ul>
        <br>
        <strong>📊 Data Sources:</strong> This application utilizes multiple data sources including Alpha Vantage API 
        and may fall back to sample data for demonstration when live APIs is unavailable.
    </div>
    """, unsafe_allow_html=True)

def display_welcome_screen():
    st.markdown(
        """
        <h2 style='text-align: center;font-size: 40px;font-weight: 800;background: -webkit-linear-gradient(45deg, #00aaff, #ff00c8);-webkit-background-clip: text;-webkit-text-fill-color: transparent;text-decoration: none;margin-bottom: 20px; font-family: "Orbitron", sans-serif;'>
            ⚔️ Ares Predictive Engine
        </h2>
        """,
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            ### ✨ Premium Features:
            - 🔄 **Multi-API Integration**: Seamless data fetching from Alpha Vantage & yfinance
            - 🤖 **Advanced AI Models**: Machine learning-powered predictions
            - 📊 **Comprehensive Analysis**: Technical indicators & market insights
            - 🎨 **Premium Interface**: Beautiful, responsive cyberpunk theme
            - 📈 **Real-time Charts**: Interactive Plotly visualizations
            - 🔍 **Performance Metrics**: Detailed model evaluation & statistics
            ### 🌍 Global Market Coverage:
            **🇺🇸 US Stocks:**
            - Apple (AAPL), Microsoft (MSFT), Alphabet/Google (GOOGL)
            - Amazon (AMZN), Tesla (TSLA), NVIDIA (NVDA)
            - Meta (META), Netflix (NFLX)
            - JPMorgan (JPM), Visa (V)
            - BlackRock (BLK), Goldman Sachs (GS), State Street (STT)
            **🇮🇳 Indian Stocks:**
            - Reliance (RELIANCE.NSE), TCS (TCS.NSE), Infosys (INFY.NSE)
            - HDFC Bank (HDFCBANK.NSE), Wipro (WIPRO.NSE), ITC (ITC.NSE)
            - SBI (SBIN.NSE), Kotak Bank (KOTAKBANK.NSE), Bharti Airtel (BHARTIARTL.NSE)
            - Hindustan Unilever (HINDUNILVR.NSE), Tata Motors (TATAMOTORS.NSE)
            - Tata Steel (TATASTEEL.NSE), Paras Defence (PARAS.NSE)
            """)
    with col2:
        st.markdown("""
            ### 🎯 How It Works:
            1. 📊 **Select Your Stock**: Pick from curated tickers or enter a custom symbol  
            2. ⏱️ **Choose Time Period**: Analyze 1 month → 5 years of data  
            3. 🤖 **AI Analysis**: ML models learn market patterns  
            4. 🔮 **Get Predictions**: Forecast next-day/multi-day prices with confidence  
            5. 📈 **Visualize Results**: Interactive charts & detailed analytics
            ### 🛠️ Technical Features:
            - 🧠 **Machine Learning**: Random Forest, Feature Engineering  
            - 🔁 **Cross-validation**: Performance metrics built-in  
            - 📊 **Technical Indicators**: Moving Averages (20/50d), RSI, Volume Analysis  
            - 📈 **Visualizations**: Interactive Price & Volume charts, RSI Momentum, Feature Importance  
            ### 💡 Pro Tips:
            - 📅 Use longer timeframes (1y+) for more reliable predictions  
            - 🌍 Consider external market/economic context  
            - ⏳ Compare predictions across different timeframes  
            - 🛡️ Always diversify your portfolio  
            """)
    st.markdown(
        """
        ---
        <p style='text-align: center; color: #00ff41;'>
        👈 Use the **sidebar** to configure your settings and begin exploring the power of **AI-driven stock prediction!**
        </p>
        """,
        unsafe_allow_html=True
    )
