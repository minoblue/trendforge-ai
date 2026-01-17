import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional

@st.cache_data(ttl=3600, show_spinner=False)
def get_stock_data(ticker: str, days: int) -> pd.DataFrame:
    """Fetch and normalize stock data with MultiIndex handling"""
    try:
        # Fetch data
        data = yf.download(ticker, period=f"{days}d", progress=False)
        
        # Flatten MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            # Remove ticker name from column labels
            data.columns = data.columns.droplevel(1)
            # Alternative: Join multi-level columns
            # data.columns = ['_'.join(col).strip() for col in data.columns.values]
        
        # Standardize column names
        data = data.rename(columns={
            'Adj Close': 'Close',
            'Close': 'Close',
            'High': 'High',
            'Low': 'Low',
            'Open': 'Open',
            'Volume': 'Volume'
        }, errors='ignore')
        
        # Fetch data with multiple fallbacks
        data = yf.download(
            ticker,
            period=f"{days}d",
            auto_adjust=True,  # Get consistent price structure
            threads=False,
            progress=False
        )

        if data.empty:
            st.error("No data received from Yahoo Finance")
            return pd.DataFrame()

        # Normalize column names
        data = data.rename(columns={
            'Adj Close': 'Close',
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low'
        }, errors='ignore')

        # Ensure numeric values
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Calculate technical indicators
        return calculate_technical_indicators(data)

    except Exception as e:
        st.error(f"Data fetch failed: {str(e)}")
        return pd.DataFrame()

def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators with null safety"""
    try:
        # Create essential columns if missing
        if 'Close' not in data.columns and 'Adj Close' in data.columns:
            data['Close'] = data['Adj Close']

        # Calculate moving averages dynamically
        for ma in [20, 50]:
            if len(data) >= ma//2:  # Require at least half the window size
                data[f'MA{ma}'] = data['Close'].rolling(
                    window=min(ma, len(data)),
                    min_periods=1
                ).mean()

        # Calculate RSI if sufficient data
        if len(data) >= 14:
            delta = data['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(14, min_periods=1).mean()
            avg_loss = loss.rolling(14, min_periods=1).mean()
            rs = avg_gain / avg_loss
            data['RSI'] = 100 - (100 / (1 + rs))

        # Calculate MACD if sufficient data
        if len(data) >= 26:
            exp12 = data['Close'].ewm(span=12, adjust=False).mean()
            exp26 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp12 - exp26
            data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

        return data.dropna(how='all')

    except Exception as e:
        st.error(f"Indicator calculation error: {str(e)}")
        return data