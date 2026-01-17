import streamlit as st
from utils.data_handler import get_stock_data
from modules import analysis, visualization, forecasting
import pandas as pd

def main():
    configure_app()
    ticker, days, page = setup_sidebar()
    data = get_stock_data(ticker, days)
    
    if data_valid(data):
        display_page(page, data, ticker, days)
    else:
        display_error()

def configure_app():
    """Configure Streamlit app settings"""
    st.set_page_config(
        page_title="TrendForge AI",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
    [data-testid="stMetricValue"] {font-size: 1.5rem !important;}
    .stPlotlyChart {border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

def setup_sidebar() -> tuple:
    """Configure sidebar elements"""
    with st.sidebar:
        st.image("image.jpg", width=300)
        st.title("TrendForge AI")
        
        ticker = st.text_input("📌 Stock Ticker", "SBIN.NS",
                             help="NSE: .NS, BSE: .BO format")
        days = st.slider("📅 Analysis Period", 1, 365, 30,
                       help="Select historical data range")
        page = st.radio("🔍 Analysis Mode", [
            "📊 Real-time Analysis",
            "📈 Visualization",
            "🔮 Forecasting"
        ])
        
        st.markdown("---")
        
    return ticker, days, page


def display_page(page: str, data: pd.DataFrame, ticker: str, days: int):
    """Route to selected page module"""
    st.header(f"Analyzing: {ticker}")
    
    if page == "📊 Real-time Analysis":
        analysis.show_analysis(data, ticker)
    elif page == "📈 Visualization":
        visualization.show_visualization(data, ticker)
    elif page == "🔮 Forecasting":
        forecasting.show_forecasting(data, ticker, days)

# Updated data_valid check
def data_valid(data: pd.DataFrame) -> bool:
    """Check if data is valid for display"""
    if data.empty:
        return False
    # Require at least 5 days of valid close prices
    close_prices = data['Close'].dropna()
    return len(close_prices) >= 5

# Updated display_error function
def display_error():
    """Show data error message with troubleshooting"""
    st.error("""
    ❗ Data Unavailable - Possible Solutions:
    1. Check internet connection
    2. Verify stock ticker format (e.g., SBIN.NS for NSE)
    3. Try a longer analysis period (minimum 5 days)
    4. Ensure market is open for live data
    """)
    st.image("https://i.imgur.com/B0gW9bD.png", width=300)

if __name__ == "__main__":
    main()