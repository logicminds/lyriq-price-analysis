#!/usr/bin/env python3
"""
Compare two CarGurus CSV files to identify new entries.
"""

import pandas as pd
import sys
from datetime import datetime

def load_and_clean_csv(file_path):
    """Load CSV file and clean the data."""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Clean column names (remove spaces, convert to lowercase)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Clean VIN column - remove any whitespace and handle NaN values
        if 'vin' in df.columns:
            df['vin'] = df['vin'].astype(str).str.strip()
            # Remove rows where VIN is 'nan' or empty
            df = df[df['vin'] != 'nan']
            df = df[df['vin'] != '']
        
        # Clean stock column
        if 'stock' in df.columns:
            df['stock'] = df['stock'].astype(str).str.strip()
        
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def compare_csv_files(file1_path, file2_path):
    """Compare two CSV files and identify new entries."""
    
    print(f"Loading {file1_path}...")
    df1 = load_and_clean_csv(file1_path)
    if df1 is None:
        return
    
    print(f"Loading {file2_path}...")
    df2 = load_and_clean_csv(file2_path)
    if df2 is None:
        return
    
    print(f"\nFile 1 ({file1_path}): {len(df1)} records")
    print(f"File 2 ({file2_path}): {len(df2)} records")
    
    # Get VINs from both files
    vins1 = set(df1['vin'].tolist()) if 'vin' in df1.columns else set()
    vins2 = set(df2['vin'].tolist()) if 'vin' in df2.columns else set()
    
    print(f"\nUnique VINs in file 1: {len(vins1)}")
    print(f"Unique VINs in file 2: {len(vins2)}")
    
    # Find new VINs in file 2 that don't exist in file 1
    new_vins = vins2 - vins1
    print(f"\nNew VINs in file 2: {len(new_vins)}")
    
    if new_vins:
        print("\nNew entries found:")
        print("=" * 80)
        
        # Get records for new VINs
        new_records = df2[df2['vin'].isin(new_vins)]
        
        # Display new records
        for idx, row in new_records.iterrows():
            print(f"\nVIN: {row['vin']}")
            print(f"Stock: {row.get('stock', 'N/A')}")
            print(f"Year: {row.get('year', 'N/A')}")
            print(f"Trim: {row.get('trim', 'N/A')}")
            print(f"Price: {row.get('price', 'N/A')}")
            print(f"Location: {row.get('location', 'N/A')}")
            print(f"Mileage: {row.get('mileage', 'N/A')}")
            print(f"Drive Type: {row.get('drive_type', 'N/A')}")
            print("-" * 40)
    
    # Find VINs that were in file 1 but not in file 2 (removed entries)
    removed_vins = vins1 - vins2
    print(f"\nVINs removed from file 1: {len(removed_vins)}")
    
    if removed_vins:
        print("\nRemoved entries:")
        print("=" * 80)
        
        # Get records for removed VINs
        removed_records = df1[df1['vin'].isin(removed_vins)]
        
        # Display removed records
        for idx, row in removed_records.iterrows():
            print(f"\nVIN: {row['vin']}")
            print(f"Stock: {row.get('stock', 'N/A')}")
            print(f"Year: {row.get('year', 'N/A')}")
            print(f"Trim: {row.get('trim', 'N/A')}")
            print(f"Price: {row.get('price', 'N/A')}")
            print(f"Location: {row.get('location', 'N/A')}")
            print("-" * 40)
    
    # Summary statistics
    print(f"\nSummary:")
    print(f"Total new entries: {len(new_vins)}")
    print(f"Total removed entries: {len(removed_vins)}")
    print(f"Net change: {len(new_vins) - len(removed_vins)}")
    
    # Analyze new entries by trim
    if new_vins:
        print(f"\nNew entries by trim:")
        trim_counts = new_records['trim'].value_counts()
        for trim, count in trim_counts.items():
            print(f"  {trim}: {count}")
        
        # Analyze new entries by year
        print(f"\nNew entries by year:")
        year_counts = new_records['year'].value_counts()
        for year, count in year_counts.items():
            print(f"  {year}: {count}")
        
        # Analyze new entries by location
        print(f"\nNew entries by location (top 10):")
        location_counts = new_records['location'].value_counts().head(10)
        for location, count in location_counts.items():
            print(f"  {location}: {count}")

def main():
    file1 = "cargurus-com-2025-10-02.csv"
    file2 = "cargurus-com-2025-10-03.csv"
    
    print("CarGurus CSV Comparison Tool")
    print("=" * 50)
    print(f"Comparing {file1} with {file2}")
    print(f"Analysis run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    compare_csv_files(file1, file2)

if __name__ == "__main__":
    main()
