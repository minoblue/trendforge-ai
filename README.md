# TrendForge AI – Intelligent Market Analysis Platform 📊🤖

**TrendForge AI** is an AI-assisted trading and market exploration tool designed to help users better understand stock price behavior through data-driven insights, predictive modeling, and interactive charts. The application is built as a lightweight web interface that blends financial data, machine learning, and natural-language reasoning into a single workflow.

It supports equities from both Indian and international markets and focuses on **clarity, interpretability, and usability** rather than raw speculation.

---

## What TrendForge AI Offers 🔍

### Market Data Exploration

* Pulls historical and near real-time stock price data
* Works with Indian market symbols as well as global tickers
* Presents structured summaries of price behavior and momentum

### Visual Trend Inspection

* Dynamic candlestick representations
* Overlay indicators such as moving averages and volume
* Smooth interactions for zooming, filtering, and comparison

### Predictive Intelligence

* Estimates future price direction using statistical models
* Highlights possible trend continuations and reversals
* Produces readable AI-generated explanations instead of raw numbers

### Thoughtful User Experience

* Minimalist layout with guided navigation
* Sidebar controls for time ranges and prediction windows
* Designed for both casual learners and serious analysts

---

## System Architecture & Tools 🧩

* **Interface Layer**: Streamlit
* **Application Logic**: Python
* **Language Model**: DeepSeek-R1 running locally via Ollama
* **Financial Data**: Yahoo Finance API
* **Charting Engine**: Plotly

---

## Getting Started 🛠️

### Requirements

* Python 3.8+
* Local LLM runtime (Ollama)

### Setup Instructions

1. Initialize the project environment

   ```bash
   git clone <repository-url>
   cd TrendForge-ai
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required libraries

   ```bash
   pip install -r requirements.txt
   ```

4. Start the AI model

   ```bash
   ollama run deepseek-r1
   ```

5. Launch the application

   ```bash
   streamlit run app/main.py
   ```

6. Open in your browser

   ```
   http://localhost:8501
   ```

---

## How Users Interact With the App 🧭

1. Provide a stock symbol

   * Indian equities: `RELIANCE.NS`, `TCS.NS`
   * International equities: `GOOGL`, `AMZN`

2. Choose a workflow

   * Market overview
   * Visual trend analysis
   * Price projection

3. Tune parameters

   * Time horizon
   * Forecast length

4. Review outcomes

   * AI interpretations
   * Trend visuals
   * Predictive insights and risk notes

---

## Codebase Layout 📁

```
TrendForge-ai/
├── app/
│   ├── main.py
│   ├── utils/
│   │   ├── data_handler.py
│   │   └── llm_helper.py
│   ├── modules/
│   │   ├── analysis.py
│   │   ├── visualization.py
│   │   └── forecasting.py
├── requirements.txt
```

---

## Practical Scenarios 🧠

* Exploring recent performance of a single stock
* Comparing price trends between two companies
* Estimating short-term price movement using AI guidance

---

## Collaboration & Extension 🤝

The project is open to enhancements such as:

* Additional technical indicators
* Improved forecasting models
* Multi-stock portfolio analysis
* Performance optimization

Contributors are welcome to extend the system responsibly.

---

## Important Note ⚠️

This application is intended for **learning, experimentation, and analytical exploration**.
It should **not be considered financial or investment advice**.

---

If you want, I can:

* Make this **sound more like a startup product**
* Rewrite it for **GitHub README vs portfolio vs resume**
* Simplify it for **non-technical users**
* Add a **problem → solution → impact narrative**

Just tell me what direction you want next 🚀
