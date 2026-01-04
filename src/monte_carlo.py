# src/monte_carlo.py
import numpy as np
import pandas as pd
from typing import Tuple, Dict

def simulate_mc(returns: pd.Series, 
                last_price: float, 
                time_horizon: int = 252, 
                simulations: int = 1000) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Runs a Monte Carlo simulation using historical return statistics (Geometric Brownian Motion).
    
    Args:
        returns (pd.Series): Historical daily returns for a single asset.
        last_price (float): The most recent closing price of the asset.
        time_horizon (int): Number of days to simulate (e.g., 252 for 1 year).
        simulations (int): Number of simulation paths to generate.
        
    Returns:
        Tuple[np.ndarray, Dict[str, float]]:
            - Simulation paths array of shape (time_horizon, simulations)
            - Summary statistics dictionary (Expected Price, Worst Case, etc.)
    """
    # Calculate drift and volatility from historical data
    # Drift = mean - 0.5 * var
    mu = returns.mean()
    sigma = returns.std()
    
    # Generate random shocks
    # Shape: (days, simulations)
    daily_shocks = np.random.normal(0, 1, (time_horizon, simulations))
    
    # Calculate daily returns for simulation
    # formula: P_t = P_{t-1} * exp((mu - 0.5 * sigma^2) + sigma * Z)
    drift = mu - 0.5 * sigma**2
    daily_sim_returns = np.exp(drift + sigma * daily_shocks)
    
    # Accumulate returns to get price paths
    price_paths = np.zeros((time_horizon, simulations))
    price_paths[0] = last_price * daily_sim_returns[0]
    
    for t in range(1, time_horizon):
        price_paths[t] = price_paths[t-1] * daily_sim_returns[t]
        
    # Analyze results at the end of the horizon
    final_prices = price_paths[-1]
    
    expected_price = np.mean(final_prices)
    median_price = np.median(final_prices)
    worst_case_5pct = np.percentile(final_prices, 5)  # 5th percentile outcome
    best_case_95pct = np.percentile(final_prices, 95)
    
    stats = {
        'Initial Price': last_price,
        'Expected Price': expected_price,
        'Median Price': median_price,
        'Worst Case (5%)': worst_case_5pct,
        'Best Case (95%)': best_case_95pct,
        'Return Mean': (expected_price / last_price) - 1,
        'Return 5%': (worst_case_5pct / last_price) - 1
    }
    
    return price_paths, stats

if __name__ == "__main__":
    # Test
    ret_series = pd.Series(np.random.normal(0.0005, 0.02, 1000))
    paths, info = simulate_mc(ret_series, last_price=100.0, time_horizon=252, simulations=100)
    print("Simulation Stats:", info)
    print("Paths shape:", paths.shape)
