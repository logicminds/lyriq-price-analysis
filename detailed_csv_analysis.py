#!/usr/bin/env python3
"""
Detailed analysis of CarGurus CSV files to understand the differences.
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

def analyze_csv_differences(file1_path, file2_path):
    """Analyze differences between two CSV files."""
    
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
    
    # Find VINs that were in file 1 but not in file 2 (removed entries)
    removed_vins = vins1 - vins2
    print(f"VINs removed from file 1: {len(removed_vins)}")
    
    # Find common VINs
    common_vins = vins1 & vins2
    print(f"Common VINs: {len(common_vins)}")
    
    # Analyze new entries
    if new_vins:
        print(f"\n=== NEW ENTRIES ANALYSIS ===")
        new_records = df2[df2['vin'].isin(new_vins)]
        
        print(f"\nNew entries by trim:")
        trim_counts = new_records['trim'].value_counts()
        for trim, count in trim_counts.items():
            print(f"  {trim}: {count}")
        
        print(f"\nNew entries by year:")
        year_counts = new_records['year'].value_counts()
        for year, count in year_counts.items():
            print(f"  {year}: {count}")
        
        print(f"\nNew entries by location (top 10):")
        location_counts = new_records['location'].value_counts().head(10)
        for location, count in location_counts.items():
            print(f"  {location}: {count}")
        
        # Show some examples of new entries
        print(f"\nSample new entries:")
        for idx, row in new_records.head(5).iterrows():
            print(f"  VIN: {row['vin']}, Trim: {row.get('trim', 'N/A')}, Year: {row.get('year', 'N/A')}, Price: {row.get('price', 'N/A')}")
    
    # Analyze removed entries
    if removed_vins:
        print(f"\n=== REMOVED ENTRIES ANALYSIS ===")
        removed_records = df1[df1['vin'].isin(removed_vins)]
        
        print(f"\nRemoved entries by trim:")
        trim_counts = removed_records['trim'].value_counts()
        for trim, count in trim_counts.items():
            print(f"  {trim}: {count}")
        
        print(f"\nRemoved entries by year:")
        year_counts = removed_records['year'].value_counts()
        for year, count in year_counts.items():
            print(f"  {year}: {count}")
        
        print(f"\nRemoved entries by location (top 10):")
        location_counts = removed_records['location'].value_counts().head(10)
        for location, count in location_counts.items():
            print(f"  {location}: {count}")
        
        # Show some examples of removed entries
        print(f"\nSample removed entries:")
        for idx, row in removed_records.head(5).iterrows():
            print(f"  VIN: {row['vin']}, Trim: {row.get('trim', 'N/A')}, Year: {row.get('year', 'N/A')}, Price: {row.get('price', 'N/A')}")
    
    # Summary statistics
    print(f"\n=== SUMMARY ===")
    print(f"Total new entries: {len(new_vins)}")
    print(f"Total removed entries: {len(removed_vins)}")
    print(f"Net change: {len(new_vins) - len(removed_vins)}")
    print(f"Common entries: {len(common_vins)}")
    
    # Check if this is actually a subset/superset situation
    if len(new_vins) == 0 and len(removed_vins) > 0:
        print(f"\n⚠️  WARNING: File 2 appears to be a SUBSET of File 1")
        print(f"   This suggests that File 2 contains fewer listings than File 1")
        print(f"   This could mean:")
        print(f"   - Some vehicles were sold/removed from listings")
        print(f"   - The search criteria changed")
        print(f"   - There was a data collection issue")
    elif len(removed_vins) == 0 and len(new_vins) > 0:
        print(f"\n✅ File 2 appears to be a SUPERSET of File 1")
        print(f"   This suggests that File 2 contains additional listings")
    elif len(new_vins) > 0 and len(removed_vins) > 0:
        print(f"\n🔄 File 2 has both new and removed entries")
        print(f"   This suggests a mixed update with some vehicles added and others removed")

def main():
    file1 = "cargurus-com-2025-10-02.csv"
    file2 = "cargurus-com-2025-10-03.csv"
    
    print("CarGurus CSV Detailed Analysis")
    print("=" * 50)
    print(f"Comparing {file1} with {file2}")
    print(f"Analysis run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    analyze_csv_differences(file1, file2)

if __name__ == "__main__":
    main()
