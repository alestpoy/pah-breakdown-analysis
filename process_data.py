#!/usr/bin/env python3
"""
Data processing script for PAH breakdown analysis.
Calculates breakdown rate from experimental data.
"""

import pandas as pd
import numpy as np
import os

def load_data(data_path):
    """Load experimental data from CSV file."""
    df = pd.read_csv(data_path)
    # Ensure required columns exist
    required_cols = ['sample_id', 'soil_moisture_pct', 'pah_concentration_start', 'pah_concentration_end']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    return df

def compute_breakdown_rate(df):
    """
    Compute breakdown rate percentage.
    breakdown_rate = ((start - end) / start) * 100
    """
    df = df.copy()
    df['breakdown_rate_raw'] = ((df['pah_concentration_start'] - df['pah_concentration_end']) /
                                df['pah_concentration_start']) * 100
    return df

def normalize_by_moisture(df):
    """
    Normalize breakdown rate by soil moisture percentage.
    Placeholder: currently returns raw breakdown rate.
    TODO: Implement moisture correction.
    """
    df['breakdown_rate_normalized'] = df['breakdown_rate_raw']
    return df

def main():
    data_file = os.path.join('data', 'experiment_data.csv')
    if not os.path.exists(data_file):
        print(f"Data file not found: {data_file}")
        # Create dummy data for testing
        print("Creating dummy data for demonstration...")
        create_dummy_data(data_file)
    
    df = load_data(data_file)
    df = compute_breakdown_rate(df)
    df = normalize_by_moisture(df)
    
    # Output results
    print("Breakdown analysis results:")
    print(df[['sample_id', 'soil_moisture_pct', 'breakdown_rate_raw', 'breakdown_rate_normalized']].head())
    
    # Save processed data
    output_file = os.path.join('data', 'processed_results.csv')
    df.to_csv(output_file, index=False)
    print(f"\nProcessed results saved to: {output_file}")

def create_dummy_data(path):
    """Generate dummy dataset for testing."""
    import pandas as pd
    np.random.seed(42)
    n_samples = 20
    dummy = pd.DataFrame({
        'sample_id': [f'S{i:03d}' for i in range(1, n_samples+1)],
        'soil_moisture_pct': np.random.uniform(10, 30, n_samples).round(1),
        'pah_concentration_start': np.random.uniform(100, 500, n_samples).round(2),
        'pah_concentration_end': np.random.uniform(10, 200, n_samples).round(2),
    })
    os.makedirs(os.path.dirname(path), exist_ok=True)
    dummy.to_csv(path, index=False)

if __name__ == '__main__':
    main()