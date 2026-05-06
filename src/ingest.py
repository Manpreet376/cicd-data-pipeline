# ingest.py
# This file reads the CSV data and validates it

import pandas as pd
import os

def load_data(filepath):
    """Read CSV file and return as dataframe"""
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"ERROR: File not found - {filepath}")
        return None
    
    # Read the CSV file
    df = pd.read_csv(filepath)
    print(f"SUCCESS: Data loaded! Shape: {df.shape}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    return df

def validate_data(df):
    """Check if data has correct columns and no issues"""
    
    # Required columns in our data
    required_columns = ['order_id', 'product', 'quantity', 'price', 'date', 'status']
    
    # Check all columns are present
    for col in required_columns:
        if col not in df.columns:
            print(f"ERROR: Missing column - {col}")
            return False
    
    print("SUCCESS: All required columns present!")
    
    # Check for empty/null values
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"WARNING: Found {null_count} empty values in data")
    else:
        print("SUCCESS: No empty values found!")
    
    # Check row count
    print(f"SUCCESS: Total records found: {len(df)}")
    
    return True

def show_preview(df):
    """Show first few rows of data"""
    print("\n--- DATA PREVIEW ---")
    print(df.head())
    print("\n--- DATA TYPES ---")
    print(df.dtypes)

# This runs when you execute the file directly
if __name__ == "__main__":
    print("=== STARTING DATA INGESTION ===\n")
    
    # Load the data
    filepath = "data/sales_data.csv"
    df = load_data(filepath)
    
    if df is not None:
        # Validate the data
        is_valid = validate_data(df)
        
        if is_valid:
            # Show preview
            show_preview(df)
            print("\n=== INGESTION COMPLETE ✅ ===")
        else:
            print("\n=== INGESTION FAILED ❌ ===")