import plotly.graph_objs as go
import streamlit as st
import pandas as pd
from typing import Optional

def show_visualization(data: pd.DataFrame, ticker: str):
    """Interactive market visualization with robust data handling"""
    st.subheader("Advanced Market Visualization")
    
    # Validate and normalize data
    data = validate_and_normalize_data(data, ticker)
    if data is None:
        return

    try:
        # Create interactive visualizations
        display_candlestick_chart(data, ticker)
        display_technical_indicators(data)
        display_volume_analysis(data)

    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
        st.write("### Debug Info:")
        st.write(f"Columns: {list(data.columns)}")
        st.write(f"Data Types:\n{data.dtypes}")
        st.write("Sample Data:", data.head(2))

def validate_and_normalize_data(data: pd.DataFrame, ticker: str) -> Optional[pd.DataFrame]:
    """Handle MultiIndex columns in validation"""
    # Flatten MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    # Normalize column names
    data.columns = data.columns.str.replace(r'_SBIN\.NS$', '', regex=True)
    
    # Check required columns
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(data.columns):
        missing = required - set(data.columns)
        st.error(f"Missing columns: {', '.join(missing)}")
        st.write("Available columns:", list(data.columns))
        return None
    
    # Rest of the validation logic...

    # Check essential price columns
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(data.columns):
        st.error(f"Missing price columns for {ticker}")
        st.write("Required columns:", required)
        st.write("Available columns:", list(data.columns))
        return None

    # Ensure datetime index
    if not isinstance(data.index, pd.DatetimeIndex):
        try:
            data.index = pd.to_datetime(data.index)
        except Exception:
            st.error("Invalid date format in index")
            return None

    # Ensure numeric values
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return data.dropna(subset=['Close'])

def display_candlestick_chart(data: pd.DataFrame, ticker: str):
    """Interactive candlestick chart with moving averages"""
    fig = go.Figure()
    
    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ))
    
    # Moving averages
    for ma in [20, 50]:
        if f'MA{ma}' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[f'MA{ma}'],
                name=f'{ma}-Day MA',
                line=dict(width=1.5)
            ))
    
    fig.update_layout(
        title=f'{ticker} Price Analysis',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        hovermode='x unified',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

def display_technical_indicators(data: pd.DataFrame):
    """Interactive technical indicator selection"""
    st.subheader("Technical Indicators")
    
    available_indicators = [
        col for col in ['MA20', 'MA50', 'RSI', 'MACD', 'Signal'] 
        if col in data.columns
    ]
    
    selected = st.multiselect(
        'Choose Indicators:',
        options=available_indicators,
        default=['MA20', 'RSI']
    )
    
    if selected:
        cols = st.columns(len(selected))
        for col, indicator in zip(cols, selected):
            with col:
                st.markdown(f"**{indicator}**")
                if indicator == 'RSI':
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data[indicator],
                        name=indicator
                    ))
                    fig.add_hline(y=30, line_dash="dot", line_color="green")
                    fig.add_hline(y=70, line_dash="dot", line_color="red")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.line_chart(data[indicator])

def display_volume_analysis(data: pd.DataFrame):
    """Volume analysis with moving average"""
    if 'Volume' in data.columns:
        st.subheader("Volume Analysis")
        vol_data = pd.DataFrame({
            'Volume': data['Volume'],
            '30D Avg': data['Volume'].rolling(30, min_periods=1).mean()
        }).dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=vol_data.index,
            y=vol_data['Volume'],
            name='Daily Volume'
        ))
        fig.add_trace(go.Scatter(
            x=vol_data.index,
            y=vol_data['30D Avg'],
            name='30D Average',
            line=dict(color='orange')
        ))
        fig.update_layout(
            height=300,
            showlegend=False,
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)