# MODIFIED charting.py
'''
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def display_charts(df, ticker, currency_symbol):
    """Display various stock charts using Plotly (Candlestick)"""
    st.markdown("### 📈 Stock Price Charts (Candlestick)")
    
    # Price chart with moving averages - NOW CANDLESTICK
    fig = go.Figure()
    
    # --- START OF CHANGE: Add the Candlestick trace ---
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Market Data'
    ))
    # --- END OF CHANGE ---

    # Moving Averages (These should still be Scatter traces)
    if 'MA_20' in df.columns and not df['MA_20'].isna().all():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], mode='lines', name='20-Day MA', line=dict(color='#ff7f0e', width=2, dash='dash')))
    if 'MA_50' in df.columns and not df['MA_50'].isna().all():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_50'], mode='lines', name='50-Day MA', line=dict(color='#2ca02c', width=2, dash='dot')))
    
    fig.update_layout(
        title=f"{ticker} Stock Price with Moving Averages (Candlestick)",
        xaxis_title="Date",
        yaxis_title=f"Price ({currency_symbol})",
        # Candlestick charts often look better without range sliders if they are the primary view
        xaxis_rangeslider_visible=False, 
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart (remains the same)
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker_color='rgba(31, 119, 180, 0.6)'))
    fig_volume.update_layout(title=f"{ticker} Trading Volume", xaxis_title="Date", yaxis_title="Volume", template='plotly_white')
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # RSI chart (remains the same)
    if 'RSI' in df.columns and not df['RSI'].isna().all():
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', line=dict(color='#d62728', width=3)))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="#ff7f0e", annotation_text="Overbought (70)")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="#2ca02c", annotation_text="Oversold (30)")
        fig_rsi.update_layout(title=f"{ticker} RSI (Relative Strength Index)", xaxis_title="Date", yaxis_title="RSI", yaxis=dict(range=[0, 100]), template='plotly_white')
        st.plotly_chart(fig_rsi, use_container_width=True)
'''

# charting.py (Final, Robust Version)

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import pandas as pd
import numpy as np # <-- CRITICAL: Ensure this is imported for the color logic
import warnings
warnings.filterwarnings('ignore')


def display_charts(df, ticker, currency_symbol):
    """
    Displays integrated Candlestick and Volume charts using subplots 
    with a dark theme, and a separate RSI chart.
    """
    
    # --- Data Validation ---
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date']
    if df is None or df.empty or not all(col in df.columns for col in required_cols):
        st.error(f"Cannot display integrated charts: Missing one or more required columns ({', '.join(required_cols)}).")
        return

    st.markdown("### 📈 Stock Price Charts")
    
    # 1. Create Subplots: 2 rows, 1 column. 
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03, # Reduced spacing for cleaner look
        row_heights=[0.7, 0.3]
    )

    # --- ROW 1: CANDLESTICK CHART with MOVING AVERAGES ---
    
    # Candlestick Trace (Row 1)
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlesticks',
        increasing_line_color='#00FF41', 
        decreasing_line_color='#FF3333', 
        # Candle fill colors
        increasing_fillcolor='rgba(0, 255, 65, 0.5)', 
        decreasing_fillcolor='rgba(255, 51, 51, 0.5)',
        showlegend=False 
    ), row=1, col=1)

    # Moving Averages (Scatter traces added to Row 1)
    if 'MA_20' in df.columns and not df['MA_20'].isna().all():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], mode='lines', name='20-Day MA', 
                                 line=dict(color='#FFA500', width=2, dash='dash')), 
                                 row=1, col=1)
    if 'MA_50' in df.columns and not df['MA_50'].isna().all():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_50'], mode='lines', name='50-Day MA', 
                                 line=dict(color='#00FFFF', width=2, dash='dot')), 
                                 row=1, col=1)

# Calculate volume bar colors
    volume_colors = np.where(df['Close'] > df['Open'], '#00FF41', '#FF3333') # Neon Green/Red
    
    # Volume Bar Trace (Row 2)
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['Volume'],
        name='Volume',
        # --- CRITICAL FINAL FIX: Use a small normalized float for width ---
        marker_color=volume_colors, 
        marker_opacity=0.8,
        width=0.8, # Setting a normalized width (0.8 works well for most Streamlit/Plotly setups)
        # --- END CRITICAL FINAL FIX ---
    ), row=2, col=1)

    # --- UPDATE LAYOUT & THEME ---
    fig.update_layout(
        title=f"{ticker} Stock Price & Volume Analysis",
        hovermode='x unified',
        template='plotly_dark', # Set the dark theme
        height=700, 
    )
    
    # Update axes titles and properties
    fig.update_yaxes(title_text=f"Price ({currency_symbol})", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    # Remove rangeslider and hide the bottom X-axis labels for the top chart
    fig.update_xaxes(showticklabels=False, row=1, col=1) 
    fig.update(layout_xaxis_rangeslider_visible=False) 
    
    # Display the main integrated chart
    st.plotly_chart(fig, use_container_width=True)
    
    # --- RSI chart (Separate Chart) ---
    '''
    if 'RSI' in df.columns and not df['RSI'].isna().all():
        st.markdown("### RSI Momentum")
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', line=dict(color='#9400D3', width=3)))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="#FF4500", annotation_text="Overbought (70)")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="#3CB371", annotation_text="Oversold (30)")
        fig_rsi.update_layout(
            title=f"{ticker} RSI (Relative Strength Index)", 
            xaxis_title="Date", 
            yaxis_title="RSI", 
            yaxis=dict(range=[0, 100]), 
            template='plotly_dark'
        )
        st.plotly_chart(fig_rsi, use_container_width=True)'''
    # charting.py - This is the final RSI chart section

    # --- RSI chart (Separate Chart) ---
    if 'RSI' in df.columns and not df['RSI'].isna().all():
        st.markdown("### RSI Momentum")
        fig_rsi = go.Figure()

        # 1. Add Shaded Neutral Zone (30 to 70)
        fig_rsi.add_hrect(y0=30, y1=70, 
                          line_width=0, 
                          fillcolor="rgba(144, 238, 144, 0.1)", # Light Green/Gray tint for neutral zone
                          layer="below")

        # 2. Add Overbought (70) and Oversold (30) Lines
        fig_rsi.add_hline(y=70, 
                          line_dash="dash", 
                          line_color="#FF4500", # Bright Orange-Red
                          line_width=2,
                          annotation_text="Overbought (70)",
                          annotation_position="top right",
                          annotation_font_color="#FF4500")
        
        fig_rsi.add_hline(y=30, 
                          line_dash="dash", 
                          line_color="#3CB371", # Medium Sea Green
                          line_width=2,
                          annotation_text="Oversold (30)",
                          annotation_position="bottom right",
                          annotation_font_color="#3CB371")
                          
        # 3. Add the RSI Line Trace
        fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], 
                                     mode='lines', name='RSI', 
                                     line=dict(color='#00FFFF', width=3))) # Bright Cyan line, thicker width

        # 4. Update Layout
        fig_rsi.update_layout(
            title=f"{ticker} RSI (Relative Strength Index)", 
            xaxis_title="Date", 
            yaxis_title="RSI", 
            yaxis=dict(range=[0, 100]), 
            template='plotly_dark'
        )
        st.plotly_chart(fig_rsi, use_container_width=True)