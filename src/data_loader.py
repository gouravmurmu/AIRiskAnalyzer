# src/data_loader.py
import yfinance as yf
import pandas as pd
from typing import List, Tuple, Optional
import os
from .config import Config

def fetch_data(tickers: List[str], start_date: str, end_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetches historical market data for the given tickers.
    
    Args:
        tickers (List[str]): List of asset tickers (e.g., ['AAPL', 'BTC-USD']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: 
            - Prices DataFrame (Adjusted Close)
            - Returns DataFrame (Log returns or simple returns, commonly simple for basic analysis)
    """
    if not tickers:
        raise ValueError("Ticker list cannot be empty.")
        
    print(f"Fetching data for: {tickers} from {start_date} to {end_date}...")
    
    try:
        # Download data
        data = yf.download(tickers, start=start_date, end=end_date, progress=False, group_by='ticker')
        
        # Structure the data
        # yfinance with group_by='ticker' returns a MultiIndex if multiple tickers, or single level if one.
        # We want a unified clean DataFrame of Adj Close prices.
        
        prices_df = pd.DataFrame()
        
        if len(tickers) == 1:
            ticker = tickers[0]
            # Handle case where single ticker might return different columns depending on yfinance version
            # Usually 'Adj Close' is present.
            if 'Adj Close' in data.columns:
                prices_df[ticker] = data['Adj Close']
            else:
                prices_df[ticker] = data['Close'] # Fallback
        else:
            for ticker in tickers:
                if (ticker, 'Adj Close') in data.columns:
                    prices_df[ticker] = data[ticker]['Adj Close']
                elif (ticker, 'Close') in data.columns:
                    prices_df[ticker] = data[ticker]['Close']
        
        # Drop missing values (e.g., weekends/holidays alignment issues)
        prices_df.dropna(inplace=True)
        
        if prices_df.empty:
            raise ValueError("No data fetched. Check tickers or date range.")
            
        # Calculate daily returns
        returns_df = prices_df.pct_change().dropna()
        
        return prices_df, returns_df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise e

if __name__ == "__main__":
    # Quick test
    cfg = Config()
    prices, ret = fetch_data(cfg.DEFAULT_TICKERS, cfg.START_DATE, cfg.END_DATE)
    print("Prices Head:\n", prices.head())
    print("Returns Head:\n", ret.head())
