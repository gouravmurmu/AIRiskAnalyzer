# src/visualizations.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
from typing import List, Dict

# Set style
try:
    sns.set_theme(style='darkgrid')
except:
    plt.style.use('ggplot')

def save_plot_to_buffer() -> BytesIO:
    """Saves the current matplotlib figure to a BytesIO buffer."""
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf

def plot_price_history(prices: pd.DataFrame) -> BytesIO:
    """Plots normalized price history."""
    plt.figure(figsize=(10, 6))
    
    # Normalize to start at 100
    normalized = (prices / prices.iloc[0]) * 100
    
    for col in normalized.columns:
        plt.plot(normalized.index, normalized[col], label=col)
        
    plt.title("Price History (Rebased to 100)")
    plt.xlabel("Date")
    plt.ylabel("Normalized Price")
    plt.legend()
    return save_plot_to_buffer()

def plot_drawdowns(prices: pd.DataFrame) -> Dict[str, BytesIO]:
    """Plots drawdowns for each asset separate or combined."""
    # Calculate drawdown
    cumulative = (1 + prices.pct_change().dropna()).cumprod()
    # Re-normalize just to be safe if not passed normalized
    cumulative = cumulative / cumulative.iloc[0] 
    
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    
    plt.figure(figsize=(10, 6))
    for col in drawdown.columns:
        plt.plot(drawdown.index, drawdown[col], label=col)
        
    plt.title("Historical Drawdowns")
    plt.xlabel("Date")
    plt.ylabel("Drawdown (%)")
    plt.legend()
    
    # Fill area heavily implies negative
    return save_plot_to_buffer()

def plot_return_distribution(returns: pd.DataFrame) -> BytesIO:
    """Plots histogram/KDE of returns."""
    plt.figure(figsize=(10, 6))
    
    for col in returns.columns:
        sns.histplot(returns[col], kde=True, label=col, alpha=0.5, bins=50)
        
    plt.title("Daily Return Distribution")
    plt.xlabel("Daily Return")
    plt.legend()
    return save_plot_to_buffer()

def plot_monte_carlo(paths: np.ndarray, ticker: str, num_lines: int = 50) -> BytesIO:
    """
    Plots Monte Carlo simulation paths.
    
    Args:
        paths (np.ndarray): Shape (time_horizon, simulations)
        ticker (str): Ticker name for title
        num_lines (int): Number of paths to plot to avoid clutter
    """
    plt.figure(figsize=(10, 6))
    
    # Plot a subset of paths
    # paths shape: (days, sims)
    # We plot columns
    subset = paths[:, :num_lines]
    
    plt.plot(subset, color='blue', alpha=0.1)
    
    # Plot mean path
    mean_path = np.mean(paths, axis=1)
    plt.plot(mean_path, color='red', linewidth=2, label='Mean Path')
    
    plt.title(f"Monte Carlo Simulation: {ticker} (Next {len(paths)} Days)")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    return save_plot_to_buffer()

if __name__ == "__main__":
    # Test
    dates = pd.date_range(start="2023-01-01", periods=100)
    data = np.random.normal(0, 0.02, (100, 2))
    df = pd.DataFrame(data, index=dates, columns=['A', 'B'])
    prices = (1 + df).cumprod() * 100
    
    print("Generating test plots...")
    plot_price_history(prices)
    plot_return_distribution(df)
    print("Plots generated in memory.")
