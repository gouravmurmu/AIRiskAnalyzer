# app.py
import argparse
import os
import pandas as pd
from src.config import Config
from src.data_loader import fetch_data
from src.risk_metrics import calculate_metrics
from src.monte_carlo import simulate_mc
from src.visualizations import plot_price_history, plot_drawdowns, plot_monte_carlo
from src.pdf_report import generate_pdf_report

def main():
    parser = argparse.ArgumentParser(description="AI Risk Analyzer for Stocks & Crypto")
    parser.add_argument('--tickers', nargs='+', default=Config.DEFAULT_TICKERS, help='List of tickers to analyze')
    parser.add_argument('--start', type=str, default=Config.START_DATE, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default=Config.END_DATE, help='End date (YYYY-MM-DD)')
    parser.add_argument('--sims', type=int, default=Config.MC_SIMULATIONS, help='Number of Monte Carlo simulations')
    
    args = parser.parse_args()
    
    print(f"--- AI Risk Analyzer ---")
    print(f"Tickers: {args.tickers}")
    print(f"Period: {args.start} to {args.end}")
    
    # 1. Fetch Data
    try:
        prices, returns = fetch_data(args.tickers, args.start, args.end)
    except Exception as e:
        print(f"Critical Error: {e}")
        return

    # 2. Calculate Risk Metrics
    print("Calculating Risk Metrics...")
    metrics = calculate_metrics(returns, risk_free_rate=Config.RISK_FREE_RATE)
    print(metrics)
    
    # 3. Monte Carlo Simulation
    print(f"Running Monte Carlo Simulation ({args.sims} runs)...")
    mc_results = {}
    mc_plots = {}
    
    for ticker in args.tickers:
        if ticker not in returns.columns:
            continue
            
        last_price = prices[ticker].iloc[-1]
        paths, stats = simulate_mc(
            returns[ticker], 
            last_price, 
            time_horizon=Config.MC_TIME_HORIZON, 
            simulations=args.sims
        )
        mc_results[ticker] = stats
        
        # Generate MC Plot
        mc_plots[f'MC_{ticker}'] = plot_monte_carlo(paths, ticker)
        
    # 4. visualizations
    print("Generating visualizations...")
    charts = {}
    charts['Price History'] = plot_price_history(prices)
    charts['Drawdowns'] = plot_drawdowns(prices)
    charts.update(mc_plots)
    
    # 5. Generate PDF
    output_path = os.path.join(Config.REPORTS_DIR, 'risk_report.pdf')
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    
    print(f"Generating Report at {output_path}...")
    generate_pdf_report(
        output_path,
        metrics,
        mc_results,
        charts
    )
    
    print("Analysis Complete.")

if __name__ == "__main__":
    main()
