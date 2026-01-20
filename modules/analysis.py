import pandas as pd
import streamlit as st
from typing import Union
from utils.llm_helper import load_llm, clean_llm_response

def safe_get_value(series, key, default: Union[str, float] = "N/A"):
    """Enhanced safe value retrieval with type checking"""
    try:
        value = series.get(key, default)
        return float(value) if pd.notnull(value) else default
    except (KeyError, TypeError, ValueError):
        return default

def format_currency(value: Union[float, str]) -> str:
    """Improved currency formatting with error handling"""
    try:
        return f"₹{float(value):,.2f}" if isinstance(value, (int, float)) else "N/A"
    except (ValueError, TypeError):
        return "N/A"

def show_analysis(data: pd.DataFrame, ticker: str):
    """Enhanced analysis module with sentiment analysis"""
    st.subheader("AI-Powered Market Analysis")
    
    if data_invalid(data):
        st.error("Invalid data format for analysis")
        return

    try:
        latest = data.iloc[-1]
        analysis_prompt = build_analysis_prompt(data, ticker)
        
        with st.spinner("🧠 Generating smart analysis..."):
            llm = load_llm()
            analysis = clean_llm_response(llm.invoke(analysis_prompt))
        
        display_results(analysis, latest, data, ticker)

    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")

def data_invalid(data: pd.DataFrame) -> bool:
    """Validate data structure"""
    return data.empty or len(data) < 1 or 'Close' not in data.columns

# Updated build_analysis_prompt function in analysis.py
def build_analysis_prompt(data: pd.DataFrame, ticker: str) -> str:
    """Construct detailed analysis prompt with safe formatting"""
    latest = data.iloc[-1]
    
    def format_value(value, format_str=".2f"):
        """Safe value formatting with fallback"""
        try:
            return f"{float(value):{format_str}}" if pd.notnull(value) else "N/A"
        except (ValueError, TypeError):
            return "N/A"
    
    return f"""
    Perform comprehensive analysis of {ticker} stock considering:
    1. Price trends (current: {format_value(latest['Close'])}, 
       20MA: {format_value(latest.get('MA20'))})
    2. Technical indicators (RSI: {format_value(latest.get('RSI'))}, 
       MACD: {format_value(latest.get('MACD'))})
    3. Recent volatility (Range: {format_value(latest['Low'])}-{format_value(latest['High'])})
    4. Volume trends (Current: {format_value(latest['Volume'], ',.0f')})

    Structure response with:
    - Trend analysis summary 📈
    - Support/resistance levels 🛡️
    - Trading strategy with entry/exit points 🎯
    - Risk assessment with stop-loss levels ⚠️
    - Fundamental health indicators 💼
    """

def display_results(analysis: str, latest: pd.Series, data: pd.DataFrame, ticker: str):
    """Display formatted analysis results"""
    st.markdown(f"## 📈 {ticker} Analysis Report")
    st.markdown(analysis)
    
    cols = st.columns(4)
    metrics = [
        ("Current Price", format_currency(latest['Close'])),
        ("Daily Change", calculate_daily_change(data)),
        ("RSI", f"{safe_get_value(latest, 'RSI', 'N/A')}"),
        ("Volume", f"{safe_get_value(latest, 'Volume', 'N/A'):,}")
    ]
    
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)

def calculate_daily_change(data: pd.DataFrame) -> str:
    """Calculate daily price change"""
    if len(data) > 1:
        prev_close = safe_get_value(data.iloc[-2], 'Close', 0)
        current_close = safe_get_value(data.iloc[-1], 'Close', 0)
        change = ((current_close - prev_close) / prev_close * 100) if prev_close else 0
        return f"{change:.2f}% ▲" if change >= 0 else f"{change:.2f}% ▼"
    return "N/A"