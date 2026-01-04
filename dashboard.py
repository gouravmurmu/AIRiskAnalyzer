# dashboard.py
import streamlit as st
import pandas as pd
import os
import tempfile
from datetime import datetime, timedelta

from src.config import Config
from src.data_loader import fetch_data
from src.risk_metrics import calculate_metrics
from src.monte_carlo import simulate_mc
from src.visualizations import plot_price_history, plot_drawdowns, plot_monte_carlo
from src.pdf_report import generate_pdf_report

st.set_page_config(page_title="AI Risk Analyzer", layout="wide")

# --- Title and Description ---
st.title("🛡️ AI Risk Analyzer")
st.markdown("""
Professional Quantitative Risk Analysis for Stocks and Crypto.
Simulate future performance, analyze drawdown risk, and generate PDF reports.
""")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")

default_tickers = "AAPL, MSFT, BTC-USD"
ticker_input = st.sidebar.text_area("Enter Tickers (comma separated)", value=default_tickers)
tickers = [t.strip() for t in ticker_input.split(',')]

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=datetime.today())

st.sidebar.subheader("Monte Carlo Settings")
sims = st.sidebar.slider("Number of Simulations", min_value=100, max_value=5000, value=1000, step=100)
horizon = st.sidebar.slider("Time Horizon (Days)", min_value=30, max_value=365, value=252)

run_btn = st.sidebar.button("Run Analysis", type="primary")

# --- Main Logic ---
if run_btn:
    with st.spinner("Fetching Market Data..."):
        try:
            # Convert dates to string for valid YYYY-MM-DD format
            s_date = start_date.strftime("%Y-%m-%d")
            e_date = end_date.strftime("%Y-%m-%d")
            
            prices, returns = fetch_data(tickers, s_date, e_date)
            st.success("Data Fetched Successfully!")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.stop()

    # --- Metrics Section ---
    st.header("1. Risk Metrics")
    metrics = calculate_metrics(returns)
    
    # Transpose for better readability in UI
    st.dataframe(metrics.T.style.format("{:.4f}"))

    # --- Visualizations Section ---
    st.header("2. Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["Price History", "Drawdowns", "Monte Carlo Simulation"])
    
    charts = {}
    
    with tab1:
        st.subheader("Price History (Rebased to 100)")
        # visualizations.py returns BytesIO, Streamlit can read it as image
        # Note: In a real interactive dash, we might prefer st.line_chart or plotly, 
        # but to reuse the "PDF-ready" chart logic exactly, using the images is a valid design choice for consistency.
        buf_price = plot_price_history(prices)
        st.image(buf_price, use_container_width=True)
        charts['Price History'] = buf_price

    with tab2:
        st.subheader("Historical Drawdowns")
        buf_dd = plot_drawdowns(prices)
        st.image(buf_dd, use_container_width=True)
        charts['Drawdowns'] = buf_dd

    with tab3:
        st.subheader(f"Monte Carlo Projections (Next {horizon} Days)")
        
        cols = st.columns(len(tickers))
        mc_results = {}
        
        for idx, ticker in enumerate(tickers):
            if ticker not in returns.columns:
                continue
                
            last_price = prices[ticker].iloc[-1]
            paths, stats = simulate_mc(returns[ticker], last_price, time_horizon=horizon, simulations=sims)
            mc_results[ticker] = stats
            
            # Plot
            buf_mc = plot_monte_carlo(paths, ticker)
            charts[f'MC_{ticker}'] = buf_mc
            
            # Display stats in column
            # Use modular logic in display
            with cols[idx % len(cols)]:
                st.image(buf_mc, caption=f"{ticker} Simulation", use_container_width=True)
                st.markdown(f"**Expected**: ${stats['Expected Price']:.2f}")
                st.markdown(f"**Worst (5%)**: ${stats['Worst Case (5%)']:.2f}")

    # --- PDF Generation ---
    st.header("3. Export Report")
    
    # We need to reset buffer pointers for the PDF generation since st.image might have consumed them? 
    # BytesIO in Python: if we read it, position moves.
    # plot functions created fresh buffers. st.image reads. 
    # We should ensure `charts` dictionary has buffers at position 0.
    for name, buf in charts.items():
        buf.seek(0)

    if st.button("Generate PDF Report"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            generate_pdf_report(tmp_file.name, metrics, mc_results, charts)
            
            with open(tmp_file.name, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                label="Download PDF Risk Report",
                data=pdf_bytes,
                file_name="risk_report.pdf",
                mime="application/pdf"
            )
