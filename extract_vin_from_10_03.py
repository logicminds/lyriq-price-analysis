#!/usr/bin/env python3
"""
Extract VIN data from the 10-03 CSV file and compare with 10-02 data.
"""

import pandas as pd
import re
from datetime import datetime

def extract_vin_from_10_03(file_path):
    """Extract VIN data from the 10-03 CSV file."""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Look for VIN patterns in the data
        vins = []
        for idx, row in df.iterrows():
            # Check each column for VIN patterns
            for col in df.columns:
                if pd.notna(row[col]):
                    cell_value = str(row[col])
                    # Look for VIN pattern (17 characters, alphanumeric)
                    vin_match = re.search(r'1GYK[A-Z0-9]{13}', cell_value)
                    if vin_match:
                        vins.append(vin_match.group())
                        break
        
        return list(set(vins))  # Remove duplicates
    except Exception as e:
        print(f"Error extracting VINs from {file_path}: {e}")
        return []

def load_10_02_vins(file_path):
    """Load VINs from the 10-02 CSV file."""
    try:
        df = pd.read_csv(file_path)
        if 'VIN' in df.columns:
            vins = df['VIN'].dropna().tolist()
            return [vin for vin in vins if vin != '']
        return []
    except Exception as e:
        print(f"Error loading VINs from {file_path}: {e}")
        return []

def compare_vin_lists(vins_10_02, vins_10_03):
    """Compare two lists of VINs."""
    set_10_02 = set(vins_10_02)
    set_10_03 = set(vins_10_03)
    
    print(f"VINs in 10-02 file: {len(set_10_02)}")
    print(f"VINs in 10-03 file: {len(set_10_03)}")
    
    # Find new VINs in 10-03
    new_vins = set_10_03 - set_10_02
    print(f"New VINs in 10-03: {len(new_vins)}")
    
    # Find VINs removed from 10-02
    removed_vins = set_10_02 - set_10_03
    print(f"VINs removed from 10-02: {len(removed_vins)}")
    
    # Find common VINs
    common_vins = set_10_02 & set_10_03
    print(f"Common VINs: {len(common_vins)}")
    
    if new_vins:
        print(f"\nNew VINs found in 10-03:")
        for vin in sorted(new_vins):
            print(f"  {vin}")
    
    if removed_vins:
        print(f"\nVINs removed from 10-02:")
        for vin in sorted(removed_vins):
            print(f"  {vin}")
    
    return {
        'new_vins': new_vins,
        'removed_vins': removed_vins,
        'common_vins': common_vins
    }

def main():
    print("CarGurus VIN Comparison Analysis")
    print("=" * 50)
    print(f"Analysis run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Extract VINs from 10-03 file
    print("Extracting VINs from 10-03 file...")
    vins_10_03 = extract_vin_from_10_03("cargurus-com-2025-10-03.csv")
    print(f"Found {len(vins_10_03)} unique VINs in 10-03 file")
    
    # Load VINs from 10-02 file
    print("Loading VINs from 10-02 file...")
    vins_10_02 = load_10_02_vins("cargurus-com-2025-10-02.csv")
    print(f"Found {len(vins_10_02)} VINs in 10-02 file")
    
    # Compare the lists
    print("\nComparing VIN lists...")
    comparison = compare_vin_lists(vins_10_02, vins_10_03)
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Total new entries: {len(comparison['new_vins'])}")
    print(f"Total removed entries: {len(comparison['removed_vins'])}")
    print(f"Net change: {len(comparison['new_vins']) - len(comparison['removed_vins'])}")
    print(f"Common entries: {len(comparison['common_vins'])}")

if __name__ == "__main__":
    main()
