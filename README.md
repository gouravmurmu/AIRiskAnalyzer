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

## Deployment (Hugging Face Spaces)

The easiest way to deploy is to push your code directly to the Space.

1.  **Create Space**:
    *   Go to [huggingface.co/new-space](https://huggingface.co/new-space).
    *   Name it `ai-risk-analyzer`.
    *   Select SDK: **Docker**.
    *   Click **Create Space**.

2.  **Push Code**:
    *   On your local machine (inside the project folder):
    ```bash
    # Replace USERNAME with your Hugging Face username
    git remote add space https://huggingface.co/spaces/USERNAME/ai-risk-analyzer
    
    # Push code to the Space
    git push space main
    ```

3.  **Launch**:
    *   The Space will build the Docker container (takes ~3 mins).
    *   Your app will be live at `https://huggingface.co/spaces/USERNAME/ai-risk-analyzer`.

### Option 2: Manual Upload (Drag & Drop)

If command line fails, you can upload files via the web interface:

1.  Go to your Space's **Files** tab.
2.  Click **Add file** -> **Upload files**.
3.  Drag and drop: `app.py`, `dashboard.py`, `Dockerfile`, `requirements.txt`, and `.dockerignore`.
4.  **Important**: For the `src` folder, you must ensure the structure is preserved. 
    *   If the web UI allows folder drag-and-drop, drag the `src` folder.
    *   If not, create a folder named `src` manually, open it, and upload the python files inside it.
5.  Commit changes. The build will start automatically.

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
