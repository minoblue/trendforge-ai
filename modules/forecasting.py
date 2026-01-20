from langchain_community.llms import Ollama
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from datetime import timedelta
from utils.llm_helper import load_llm, clean_llm_response
import plotly.graph_objects as go

def show_forecasting(data: pd.DataFrame, ticker: str, days: int):
    """Enhanced forecasting module with robust formatting"""
    st.subheader("AI-Powered Price Forecasting")
    
    try:
        # Clean and validate data
        data = preprocess_forecast_data(data)
        if data is None or len(data) < 5:
            st.error("Minimum 5 days of closing prices required")
            return

        # Display AI analysis
        display_llm_forecast(data, ticker, days)
        
        # Display ML predictions
        display_ml_forecast(data, ticker)

    except Exception as e:
        st.error(f"Forecasting error: {str(e)}")
        st.write("Debug Info:", data.columns if not data.empty else "Empty DataFrame")

def preprocess_forecast_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare data for forecasting"""
    if data.empty or 'Close' not in data.columns:
        return None
    
    # Handle MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    # Ensure numeric format
    numeric_data = data[['Close']].apply(pd.to_numeric, errors='coerce').dropna()
    return numeric_data

def display_llm_forecast(data: pd.DataFrame, ticker: str, days: int):
    """Display LLM-based forecast with safe formatting"""
    st.subheader("AI Market Prediction")
    
    with st.spinner("🔮 Analyzing market trends..."):
        try:
            llm = load_llm()
            prompt = build_forecast_prompt(data, ticker, days)
            forecast = clean_llm_response(llm.invoke(prompt))
            
            st.markdown(f"### 🌟 {ticker} Forecast Insights")
            st.markdown(forecast)
            
        except Exception as e:
            st.error("Failed to generate AI forecast")
            st.error(f"Error details: {str(e)}")

def build_forecast_prompt(data: pd.DataFrame, ticker: str, days: int) -> str:
    """Build forecast prompt with safe value formatting"""
    def safe_format(value, default="N/A"):
        """Format values safely for LLM prompt"""
        try:
            if isinstance(value, (int, float)):
                return f"{value:.2f}"
            return str(default)
        except:
            return str(default)

    return f"""
    Analyze {ticker} stock with:
    - Current Price: {safe_format(data['Close'].iloc[-1])}
    - Recent Trend: {safe_format(data['Close'].pct_change(7).mean() * 100)}% (7D avg)
    - Volatility: {safe_format(data['Close'].std())}
    - Analysis Period: {len(data)} days

    Provide:
    1. Price prediction for next {days} days
    2. Key technical drivers
    3. Recommended entry/exit points
    4. Risk assessment
    """

def display_ml_forecast(data: pd.DataFrame, ticker: str):
    """Display machine learning forecasts"""
    st.subheader("Algorithmic Projections")
    
    days = st.slider("Forecast Horizon (days)", 1, 90, 30)
    model_type = st.selectbox("Prediction Model", 
                            ["Linear Regression", "Polynomial Regression"])
    
    try:
        forecast = generate_ml_forecast(data, days, model_type)
        if not forecast.empty:
            display_forecast_results(data, forecast, ticker)
            
    except Exception as e:
        st.error("Algorithmic prediction failed")
        st.error(f"Technical error: {str(e)}")

def generate_ml_forecast(data: pd.DataFrame, days: int, model: str) -> pd.DataFrame:
    """Generate ML forecast with error handling"""
    X = np.arange(len(data)).reshape(-1, 1)
    y = data['Close'].values
    
    if model == "Polynomial Regression":
        model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    else:
        model = LinearRegression()
        
    model.fit(X, y)
    future = np.arange(len(X), len(X)+days).reshape(-1, 1)
    dates = pd.date_range(data.index[-1] + timedelta(1), periods=days)
    
    return pd.DataFrame({
        'Date': dates,
        'Predicted Close': model.predict(future)
    }).set_index('Date')

def display_forecast_results(history: pd.DataFrame, forecast: pd.DataFrame, ticker: str):
    """Visualize forecast results"""
    combined = pd.concat([history[['Close']], forecast], axis=0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history.index,
        y=history['Close'],
        name='Historical Prices',
        line=dict(color='royalblue')
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index,
        y=forecast['Predicted Close'],
        name='Forecast',
        line=dict(color='firebrick', dash='dot')
    ))
    fig.update_layout(
        title=f'{ticker} Price Forecast',
        height=500,
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("Detailed Predictions:")
    st.dataframe(forecast.style.format("{:.2f}"))