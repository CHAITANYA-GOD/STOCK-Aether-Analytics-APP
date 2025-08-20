import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def display_charts(df, ticker, currency_symbol):
    """Display various stock charts using Plotly"""
    st.markdown("### 📈 Stock Price Charts")
    
    # Price chart with moving averages
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price', line=dict(color='#1f77b4', width=3)))
    if 'MA_20' in df.columns and not df['MA_20'].isna().all():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], mode='lines', name='20-Day MA', line=dict(color='#ff7f0e', width=2, dash='dash')))
    if 'MA_50' in df.columns and not df['MA_50'].isna().all():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_50'], mode='lines', name='50-Day MA', line=dict(color='#2ca02c', width=2, dash='dot')))
    
    fig.update_layout(
        title=f"{ticker} Stock Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title=f"Price ({currency_symbol})",
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker_color='rgba(31, 119, 180, 0.6)'))
    fig_volume.update_layout(title=f"{ticker} Trading Volume", xaxis_title="Date", yaxis_title="Volume", template='plotly_white')
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # RSI chart
    if 'RSI' in df.columns and not df['RSI'].isna().all():
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', line=dict(color='#d62728', width=3)))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="#ff7f0e", annotation_text="Overbought (70)")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="#2ca02c", annotation_text="Oversold (30)")
        fig_rsi.update_layout(title=f"{ticker} RSI (Relative Strength Index)", xaxis_title="Date", yaxis_title="RSI", yaxis=dict(range=[0, 100]), template='plotly_white')
        st.plotly_chart(fig_rsi, use_container_width=True)