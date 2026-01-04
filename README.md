# AI Risk Analyzer

A production-grade Python system for quantitative risk analysis of stocks and cryptocurrencies. This tool evaluates historical risk metrics, performs Monte Carlo simulations for future price path forecasting, and generates professional PDF reports for investment analysis.

## Features

- **Multi-Asset Support**: Seamlessly handles stocks (AAPl, MSFT) and crypto (BTC-USD, ETH-USD).
- **Risk Metrics Engine**: Calculates Vectorized Annualized Volatility, Max Drawdown, Sharpe Ratio, VaR (95%), and CVaR.
- **Monte Carlo Simulation**: Simulates thousands of future price paths using Geometric Brownian Motion to estimate downside risk.
- **Automated Reporting**: Generates client-ready PDF reports with embedded visualization and executive summaries.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the analyzer with default settings:
```bash
python app.py
```

Customize tickers and date range:
```bash
python app.py --tickers NVDA GOOGL BTC-USD --start 2022-01-01 --end 2024-01-01 --sims 5000
```

### Streamlit Dashboard (Interactive UI)

For a visual, interactive experience:
```bash
streamlit run dashboard.py
```

## Project Structure

- `src/data_loader.py`: Fetches market data using yfinance.
- `src/risk_metrics.py`: Computes financial ratios and risk indicators.
- `src/monte_carlo.py`: Stochastic simulation engine.
- `src/visualizations.py`: Generates plotting assets.
- `src/pdf_report.py`: reportlab PDF generation pipeline.

## Financial Metrics Explained

- **Sharpe Ratio**: A measure of risk-adjusted return. Higher is better.
- **Max Drawdown**: The maximum observed loss from a peak to a trough.
- **VaR (95%)**: Value at Risk. The maximum loss expected 95% of the time.
