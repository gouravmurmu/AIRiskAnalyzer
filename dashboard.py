# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

from src.config import Config
from src.data_loader import fetch_data
from src.risk_metrics import calculate_metrics
from src.monte_carlo import simulate_mc
from src.visualizations import plot_price_history, plot_drawdowns, plot_monte_carlo

st.set_page_config(page_title="AI Risk Analyzer", layout="wide")

# --- CSS for Report Style ---
st.markdown("""
<style>
    .report-title { font-size: 3em; font-weight: bold; color: #2C3E50; margin-bottom: 0px; }
    .report-subtitle { font-size: 1.2em; color: #7F8C8D; margin-bottom: 20px; }
    .section-header { font-size: 1.8em; font-weight: bold; color: #2980B9; border-bottom: 2px solid #2980B9; margin-top: 30px; margin-bottom: 15px; }
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #e9ecef; }
    .stDataFrame { margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- CSS for UI Stabilization ---
st.markdown("""
<style>
    /* Force vertical scrollbar to always show, preventing layout shift (shaking) */
    html { overflow-y: scroll; }
    
    /* Stabilize main container padding */
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
    
    /* Ensure images don't overflow causing horizontal shake */
    img { max-width: 100%; }
</style>
""", unsafe_allow_html=True)

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
    with st.spinner("Analyzing Market Data..."):
        try:
            s_date = start_date.strftime("%Y-%m-%d")
            e_date = end_date.strftime("%Y-%m-%d")
            prices, returns = fetch_data(tickers, s_date, e_date)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.stop()

    # --- Calculations ---
    metrics = calculate_metrics(returns)
    mc_results = {}
    mc_plots = {}
    
    for ticker in tickers:
        if ticker in returns.columns:
            last_price = prices[ticker].iloc[-1]
            paths, stats = simulate_mc(returns[ticker], last_price, time_horizon=horizon, simulations=sims)
            mc_results[ticker] = stats
            mc_plots[ticker] = plot_monte_carlo(paths, ticker)

    # --- Report View ---
    
    # Title Section
    st.markdown('<div class="report-title">AI Risk Analysis Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-subtitle">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")} | Period: {s_date} to {e_date}</div>', unsafe_allow_html=True)

    # 1. Executive Summary
    st.markdown('<div class="section-header">1. Executive Summary</div>', unsafe_allow_html=True)
    
    # Dynamic Summary Text
    best_asset = metrics.loc['Total Return'].idxmax()
    worst_asset = metrics.loc['Max Drawdown'].idxmin() # Most negative
    highest_vol = metrics.loc['Annualized Volatility'].idxmax()
    
    summary_text = f"""
    This report analyzes the risk and performance profile of **{len(tickers)} assets**. 
    Over the selected period, **{best_asset}** delivered the highest cumulative return, while **{worst_asset}** experienced the most significant drawdown.
    
    **Volatility Analysis:** {highest_vol} showed the highest annualized volatility, indicating it was the riskiest asset in historical terms.
    
    **Forward Outlook:** Monte Carlo simulations ({sims} runs) have been projected for the next {horizon} days to estimate potential downside risks (VaR) and expected price targets.
    """
    st.markdown(summary_text)

    # 2. Risk Metrics Table
    st.markdown('<div class="section-header">2. Historical Risk Metrics</div>', unsafe_allow_html=True)
    st.dataframe(metrics.T.style.format("{:.4f}").background_gradient(cmap='RdYlGn', subset=['Total Return', 'Sharpe Ratio']).background_gradient(cmap='RdYlGn_r', subset=['Annualized Volatility', 'Max Drawdown', 'VaR (95%)']), use_container_width=True)

    # 3. Visualizations Layout
    st.markdown('<div class="section-header">3. Market Visualization</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price History (Rebased to 100)")
        st.image(plot_price_history(prices), use_container_width=True)
        
    with col2:
        st.subheader("Historical Drawdowns")
        st.image(plot_drawdowns(prices), use_container_width=True)

    # 4. Monte Carlo Breakdown
    st.markdown('<div class="section-header">4. Monte Carlo Future Projections</div>', unsafe_allow_html=True)
    st.markdown(f"Projections for the next **{horizon} days** based on {sims} simulations.")
    
    for ticker in tickers:
        if ticker in mc_results:
            stats = mc_results[ticker]
            
            with st.container():
                st.markdown(f"### {ticker}")
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <b>Expected Price:</b> ${stats['Expected Price']:.2f}<br>
                        <b>Upside (95%):</b> ${stats['Best Case (95%)']:.2f}<br>
                        <b style="color:red">Downside (5%):</b> ${stats['Worst Case (5%)']:.2f}<br>
                        <b>Exp. Return:</b> {stats['Return Mean']:.1%}
                    </div>
                    """, unsafe_allow_html=True)
                    
                with c2:
                    st.image(mc_plots[ticker], use_container_width=True)
                
                st.divider()

else:
    st.info("👈 Enter tickers and click 'Run Analysis' to generate the report.")
