#!/usr/bin/env python3
"""
Extract new entries from 10-03 CSV file and normalize to JSON format.
"""

import pandas as pd
import json
import re
from datetime import datetime
from typing import Dict, List, Any

def extract_price_number(price_str: str) -> int:
    """Extract numeric price from string."""
    if not price_str or pd.isna(price_str):
        return 0
    
    # Remove currency symbols and commas
    price_clean = re.sub(r'[$,]', '', str(price_str))
    
    # Extract first number found
    match = re.search(r'\d+', price_clean)
    if match:
        return int(match.group())
    return 0

def extract_mileage_number(mileage_str: str) -> int:
    """Extract numeric mileage from string."""
    if not mileage_str or pd.isna(mileage_str):
        return 0
    
    # Remove commas and extract number
    mileage_clean = re.sub(r'[,]', '', str(mileage_str))
    match = re.search(r'\d+', mileage_clean)
    if match:
        return int(match.group())
    return 0

def extract_payment_number(payment_str: str) -> int:
    """Extract numeric payment from string."""
    if not payment_str or pd.isna(payment_str):
        return 0
    
    # Extract number from payment string like "$670/mo est."
    match = re.search(r'\$(\d+)', str(payment_str))
    if match:
        return int(match.group(1))
    return 0

def extract_year_number(year_str: str) -> int:
    """Extract numeric year from string."""
    if not year_str or pd.isna(year_str):
        return 0
    
    # Extract 4-digit year
    match = re.search(r'(\d{4})', str(year_str))
    if match:
        return int(match.group(1))
    return 0

def convert_drive_type(drive_type: str) -> str:
    """Convert drive type to abbreviation."""
    if not drive_type or pd.isna(drive_type):
        return ""
    
    drive_type = str(drive_type).strip()
    if "All-Wheel Drive" in drive_type:
        return "AWD"
    elif "Rear-Wheel Drive" in drive_type:
        return "RWD"
    elif "Front-Wheel Drive" in drive_type:
        return "FWD"
    return drive_type

def clean_trim_field(trim: str) -> str:
    """Clean trim field by removing AWD/RWD suffixes."""
    if not trim or pd.isna(trim):
        return ""
    
    trim = str(trim).strip()
    # Remove AWD/RWD suffixes to avoid duplication
    trim = re.sub(r'\s+(AWD|RWD)$', '', trim)
    return trim

def extract_new_entries_from_10_03():
    """Extract new entries from 10-03 CSV file and normalize to JSON format."""
    
    # Load the 10-02 JSON file to get existing VINs
    print("Loading existing VINs from 10-02 JSON file...")
    try:
        with open('cargurus-com-2025-10-02-final.json', 'r') as f:
            existing_data = json.load(f)
        existing_vins = {record['vin'] for record in existing_data if 'vin' in record}
        print(f"Found {len(existing_vins)} existing VINs")
    except Exception as e:
        print(f"Error loading existing JSON: {e}")
        existing_vins = set()
    
    # Load the 10-03 CSV file
    print("Loading 10-03 CSV file...")
    try:
        df = pd.read_csv('cargurus-com-2025-10-03.csv')
        print(f"Loaded {len(df)} records from 10-03 CSV")
    except Exception as e:
        print(f"Error loading 10-03 CSV: {e}")
        return []
    
    # Extract VINs and find new entries
    new_entries = []
    current_time = datetime.now().isoformat()
    
    for idx, row in df.iterrows():
        # Look for VIN in the row
        vin = None
        for col in df.columns:
            if pd.notna(row[col]):
                cell_value = str(row[col])
                vin_match = re.search(r'1GYK[A-Z0-9]{13}', cell_value)
                if vin_match:
                    vin = vin_match.group()
                    break
        
        if vin and vin not in existing_vins:
            print(f"Processing new VIN: {vin}")
            
            # Extract data using specific column mappings
            record = {
                "vin": vin,
                "stock": str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else "",  # 7th column (index 6)
                "mileage": extract_mileage_number(str(row.iloc[8])) if pd.notna(row.iloc[8]) else 0,  # 9th column (index 8)
                "interior_color": str(row.iloc[10]).strip() if pd.notna(row.iloc[10]) else "",  # 11th column (index 10)
                "exterior_color": str(row.iloc[12]).strip() if pd.notna(row.iloc[12]) else "",  # 13th column (index 12)
                "drive_type": convert_drive_type(str(row.iloc[14])) if pd.notna(row.iloc[14]) else "",  # 15th column (index 14)
                "model": "LYRIQ",
                "make": "Cadillac",
                "request_info": str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else "(111) 111-1111",  # phone column
                "photo": str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else "",  # 4th column (index 3)
                "year": extract_year_number(str(row.get('data28', ''))) if pd.notna(row.get('data28')) else 0,  # data28 column
                "location": str(row.get('data32', '')).strip() if pd.notna(row.get('data32')) else "",  # data32 column
                "payment": extract_payment_number(str(row.get('data33', ''))) if pd.notna(row.get('data33')) else 0,  # data33 column
                "trim": clean_trim_field(str(row.get('title', '')).strip()) if pd.notna(row.get('title')) else "",  # title column
                "price": extract_price_number(str(row.get('price', ''))) if pd.notna(row.get('price')) else 0,  # price column
                "time": current_time
            }
            
            # Handle LYRIQ-V model conversion
            if record["model"] == "LYRIQ-V":
                record["trim"] = "V-Series"
            
            new_entries.append(record)
    
    return new_entries

def main():
    print("Extracting New Entries from 10-03 CSV")
    print("=" * 50)
    
    new_entries = extract_new_entries_from_10_03()
    
    print(f"\nFound {len(new_entries)} new entries")
    
    if new_entries:
        # Save to JSON file
        output_file = "new_entries_10_03.json"
        with open(output_file, 'w') as f:
            json.dump(new_entries, f, indent=2)
        print(f"Saved new entries to {output_file}")
        
        # Display summary
        print(f"\nSummary of new entries:")
        print(f"Total new entries: {len(new_entries)}")
        
        # Count by trim
        trim_counts = {}
        for entry in new_entries:
            trim = entry.get('trim', 'Unknown')
            trim_counts[trim] = trim_counts.get(trim, 0) + 1
        
        print(f"\nNew entries by trim:")
        for trim, count in sorted(trim_counts.items()):
            print(f"  {trim}: {count}")
        
        # Count by year
        year_counts = {}
        for entry in new_entries:
            year = entry.get('year', 0)
            year_counts[year] = year_counts.get(year, 0) + 1
        
        print(f"\nNew entries by year:")
        for year, count in sorted(year_counts.items()):
            print(f"  {year}: {count}")
        
        # Show sample entries
        print(f"\nSample new entries:")
        for i, entry in enumerate(new_entries[:3]):
            print(f"  {i+1}. VIN: {entry['vin']}, Trim: {entry['trim']}, Year: {entry['year']}, Price: ${entry['price']}, Location: {entry['location']}")
    
    else:
        print("No new entries found")

if __name__ == "__main__":
    main()
