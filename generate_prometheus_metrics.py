#!/usr/bin/env python3
"""
Generate Prometheus metrics from vehicle data for Grafana Cloud.
Converts JSON data into Prometheus metrics format.
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter, defaultdict

def load_vehicle_data(json_file: str) -> List[Dict]:
    """Load vehicle data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return []

def generate_prometheus_metrics(data: List[Dict], output_file: str):
    """Generate Prometheus metrics from vehicle data."""
    
    if not data:
        print("No data to process")
        return
    
    metrics = []
    timestamp = int(datetime.now().timestamp() * 1000)  # milliseconds
    
    # Vehicle count metrics
    total_vehicles = len(data)
    metrics.append(f"lyriq_vehicles_total {total_vehicles} {timestamp}")
    
    # Price metrics
    prices = [record.get('price', 0) for record in data if record.get('price', 0) > 0]
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        metrics.append(f"lyriq_price_average {avg_price:.2f} {timestamp}")
        metrics.append(f"lyriq_price_min {min_price} {timestamp}")
        metrics.append(f"lyriq_price_max {max_price} {timestamp}")
    
    # Mileage metrics
    mileages = [record.get('mileage', 0) for record in data if record.get('mileage', 0) > 0]
    if mileages:
        avg_mileage = sum(mileages) / len(mileages)
        min_mileage = min(mileages)
        max_mileage = max(mileages)
        
        metrics.append(f"lyriq_mileage_average {avg_mileage:.2f} {timestamp}")
        metrics.append(f"lyriq_mileage_min {min_mileage} {timestamp}")
        metrics.append(f"lyriq_mileage_max {max_mileage} {timestamp}")
    
    # Year distribution
    year_counts = Counter(record.get('year', 0) for record in data)
    for year, count in year_counts.items():
        if year > 0:
            metrics.append(f'lyriq_vehicles_by_year{{year="{year}"}} {count} {timestamp}')
    
    # Trim distribution
    trim_counts = Counter(record.get('trim', '') for record in data)
    for trim, count in trim_counts.items():
        if trim:
            # Clean trim name for metric labels
            clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
            metrics.append(f'lyriq_vehicles_by_trim{{trim="{clean_trim}"}} {count} {timestamp}')
    
    # Location distribution (by state)
    location_counts = Counter()
    for record in data:
        location = record.get('location', '')
        if location and ',' in location:
            state = location.split(',')[-1].strip()
            location_counts[state] += 1
    
    for state, count in location_counts.items():
        clean_state = state.replace(' ', '_').lower()
        metrics.append(f'lyriq_vehicles_by_state{{state="{clean_state}"}} {count} {timestamp}')
    
    # Drive type distribution
    drive_counts = Counter(record.get('drive_type', '') for record in data)
    for drive_type, count in drive_counts.items():
        if drive_type:
            clean_drive = drive_type.replace(' ', '_').lower()
            metrics.append(f'lyriq_vehicles_by_drive_type{{drive_type="{clean_drive}"}} {count} {timestamp}')
    
    # Interior color distribution
    interior_counts = Counter(record.get('interior_color', '') for record in data)
    for color, count in interior_counts.items():
        if color:
            clean_color = color.replace(' ', '_').replace('-', '_').lower()
            metrics.append(f'lyriq_vehicles_by_interior_color{{color="{clean_color}"}} {count} {timestamp}')
    
    # Exterior color distribution
    exterior_counts = Counter(record.get('exterior_color', '') for record in data)
    for color, count in exterior_counts.items():
        if color:
            clean_color = color.replace(' ', '_').replace('-', '_').lower()
            metrics.append(f'lyriq_vehicles_by_exterior_color{{color="{clean_color}"}} {count} {timestamp}')
    
    # Price ranges
    price_ranges = {
        'under_40k': 0,
        '40k_50k': 0,
        '50k_60k': 0,
        'over_60k': 0
    }
    
    for record in data:
        price = record.get('price', 0)
        if price > 0:
            if price < 40000:
                price_ranges['under_40k'] += 1
            elif price < 50000:
                price_ranges['40k_50k'] += 1
            elif price < 60000:
                price_ranges['50k_60k'] += 1
            else:
                price_ranges['over_60k'] += 1
    
    for range_name, count in price_ranges.items():
        metrics.append(f'lyriq_vehicles_by_price_range{{range="{range_name}"}} {count} {timestamp}')
    
    # Mileage ranges (2500-mile increments)
    mileage_ranges = {
        '0_2500': 0,
        '2500_5000': 0,
        '5000_7500': 0,
        '7500_10000': 0,
        '10000_12500': 0,
        '12500_15000': 0,
        '15000_17500': 0,
        '17500_20000': 0,
        '20000_22500': 0,
        '22500_25000': 0,
        '25000_27500': 0,
        '27500_30000': 0,
        '30000_32500': 0,
        '32500_35000': 0,
        '35000_37500': 0,
        '37500_40000': 0,
        'over_40000': 0
    }
    
    for record in data:
        mileage = record.get('mileage', 0)
        if mileage > 0:
            if mileage < 2500:
                mileage_ranges['0_2500'] += 1
            elif mileage < 5000:
                mileage_ranges['2500_5000'] += 1
            elif mileage < 7500:
                mileage_ranges['5000_7500'] += 1
            elif mileage < 10000:
                mileage_ranges['7500_10000'] += 1
            elif mileage < 12500:
                mileage_ranges['10000_12500'] += 1
            elif mileage < 15000:
                mileage_ranges['12500_15000'] += 1
            elif mileage < 17500:
                mileage_ranges['15000_17500'] += 1
            elif mileage < 20000:
                mileage_ranges['17500_20000'] += 1
            elif mileage < 22500:
                mileage_ranges['20000_22500'] += 1
            elif mileage < 25000:
                mileage_ranges['22500_25000'] += 1
            elif mileage < 27500:
                mileage_ranges['25000_27500'] += 1
            elif mileage < 30000:
                mileage_ranges['27500_30000'] += 1
            elif mileage < 32500:
                mileage_ranges['30000_32500'] += 1
            elif mileage < 35000:
                mileage_ranges['32500_35000'] += 1
            elif mileage < 37500:
                mileage_ranges['35000_37500'] += 1
            elif mileage < 40000:
                mileage_ranges['37500_40000'] += 1
            else:
                mileage_ranges['over_40000'] += 1
    
    for range_name, count in mileage_ranges.items():
        metrics.append(f'lyriq_vehicles_by_mileage_range{{range="{range_name}"}} {count} {timestamp}')
    
    # Payment metrics
    payments = [record.get('payment', 0) for record in data if record.get('payment', 0) > 0]
    if payments:
        avg_payment = sum(payments) / len(payments)
        min_payment = min(payments)
        max_payment = max(payments)
        
        metrics.append(f"lyriq_payment_average {avg_payment:.2f} {timestamp}")
        metrics.append(f"lyriq_payment_min {min_payment} {timestamp}")
        metrics.append(f"lyriq_payment_max {max_payment} {timestamp}")
    
    # Trim by state metrics
    trim_by_state = defaultdict(lambda: defaultdict(int))
    for record in data:
        location = record.get('location', '')
        trim = record.get('trim', '')
        if location and trim and ',' in location:
            state = location.split(',')[-1].strip()
            if state and trim:
                clean_state = state.replace(' ', '_').lower()
                clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
                trim_by_state[clean_state][clean_trim] += 1
    
    for state, trims in trim_by_state.items():
        for trim, count in trims.items():
            metrics.append(f'lyriq_vehicles_by_trim_state{{state="{state}",trim="{trim}"}} {count} {timestamp}')
    
    # Year by state metrics
    year_by_state = defaultdict(lambda: defaultdict(int))
    for record in data:
        location = record.get('location', '')
        year = record.get('year', 0)
        if location and year > 0 and ',' in location:
            state = location.split(',')[-1].strip()
            if state:
                clean_state = state.replace(' ', '_').lower()
                year_by_state[clean_state][str(year)] += 1
    
    for state, years in year_by_state.items():
        for year, count in years.items():
            metrics.append(f'lyriq_vehicles_by_year_state{{state="{state}",year="{year}"}} {count} {timestamp}')
    
    # Drive type by state metrics
    drive_by_state = defaultdict(lambda: defaultdict(int))
    for record in data:
        location = record.get('location', '')
        drive_type = record.get('drive_type', '')
        if location and drive_type and ',' in location:
            state = location.split(',')[-1].strip()
            if state:
                clean_state = state.replace(' ', '_').lower()
                clean_drive = drive_type.replace(' ', '_').lower()
                drive_by_state[clean_state][clean_drive] += 1
    
    for state, drives in drive_by_state.items():
        for drive, count in drives.items():
            metrics.append(f'lyriq_vehicles_by_drive_state{{state="{state}",drive_type="{drive}"}} {count} {timestamp}')
    
    # Price by state metrics
    price_by_state = defaultdict(list)
    for record in data:
        location = record.get('location', '')
        price = record.get('price', 0)
        if location and price > 0 and ',' in location:
            state = location.split(',')[-1].strip()
            if state:
                clean_state = state.replace(' ', '_').lower()
                price_by_state[clean_state].append(price)
    
    for state, prices in price_by_state.items():
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            metrics.append(f'lyriq_price_by_state{{state="{state}"}} {avg_price:.2f} {timestamp}')
            metrics.append(f'lyriq_price_min_by_state{{state="{state}"}} {min_price} {timestamp}')
            metrics.append(f'lyriq_price_max_by_state{{state="{state}"}} {max_price} {timestamp}')
    
    # Mileage by state metrics
    mileage_by_state = defaultdict(list)
    for record in data:
        location = record.get('location', '')
        mileage = record.get('mileage', 0)
        if location and mileage > 0 and ',' in location:
            state = location.split(',')[-1].strip()
            if state:
                clean_state = state.replace(' ', '_').lower()
                mileage_by_state[clean_state].append(mileage)
    
    for state, mileages in mileage_by_state.items():
        if mileages:
            avg_mileage = sum(mileages) / len(mileages)
            min_mileage = min(mileages)
            max_mileage = max(mileages)
            metrics.append(f'lyriq_mileage_by_state{{state="{state}"}} {avg_mileage:.2f} {timestamp}')
            metrics.append(f'lyriq_mileage_min_by_state{{state="{state}"}} {min_mileage} {timestamp}')
            metrics.append(f'lyriq_mileage_max_by_state{{state="{state}"}} {max_mileage} {timestamp}')
    
    # Interior/Exterior color combinations
    color_combinations = defaultdict(int)
    for record in data:
        interior = record.get('interior_color', '')
        exterior = record.get('exterior_color', '')
        if interior and exterior:
            clean_interior = interior.replace(' ', '_').replace('-', '_').lower()
            clean_exterior = exterior.replace(' ', '_').replace('-', '_').lower()
            combo = f"{clean_interior}_{clean_exterior}"
            color_combinations[combo] += 1
    
    for combo, count in color_combinations.items():
        metrics.append(f'lyriq_vehicles_by_color_combo{{combo="{combo}"}} {count} {timestamp}')
    
    # Year by trim metrics
    year_by_trim = defaultdict(lambda: defaultdict(int))
    for record in data:
        year = record.get('year', 0)
        trim = record.get('trim', '')
        if year > 0 and trim:
            clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
            year_by_trim[clean_trim][str(year)] += 1
    
    for trim, years in year_by_trim.items():
        for year, count in years.items():
            metrics.append(f'lyriq_vehicles_by_trim_year{{trim="{trim}",year="{year}"}} {count} {timestamp}')
    
    # Price by trim metrics
    price_by_trim = defaultdict(list)
    for record in data:
        trim = record.get('trim', '')
        price = record.get('price', 0)
        if trim and price > 0:
            clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
            price_by_trim[clean_trim].append(price)
    
    for trim, prices in price_by_trim.items():
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            metrics.append(f'lyriq_price_by_trim{{trim="{trim}"}} {avg_price:.2f} {timestamp}')
            metrics.append(f'lyriq_price_min_by_trim{{trim="{trim}"}} {min_price} {timestamp}')
            metrics.append(f'lyriq_price_max_by_trim{{trim="{trim}"}} {max_price} {timestamp}')
    
    # Mileage by trim metrics
    mileage_by_trim = defaultdict(list)
    for record in data:
        trim = record.get('trim', '')
        mileage = record.get('mileage', 0)
        if trim and mileage > 0:
            clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
            mileage_by_trim[clean_trim].append(mileage)
    
    for trim, mileages in mileage_by_trim.items():
        if mileages:
            avg_mileage = sum(mileages) / len(mileages)
            min_mileage = min(mileages)
            max_mileage = max(mileages)
            metrics.append(f'lyriq_mileage_by_trim{{trim="{trim}"}} {avg_mileage:.2f} {timestamp}')
            metrics.append(f'lyriq_mileage_min_by_trim{{trim="{trim}"}} {min_mileage} {timestamp}')
            metrics.append(f'lyriq_mileage_max_by_trim{{trim="{trim}"}} {max_mileage} {timestamp}')
    
    # Payment by trim metrics
    payment_by_trim = defaultdict(list)
    for record in data:
        trim = record.get('trim', '')
        payment = record.get('payment', 0)
        if trim and payment > 0:
            clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
            payment_by_trim[clean_trim].append(payment)
    
    for trim, payments in payment_by_trim.items():
        if payments:
            avg_payment = sum(payments) / len(payments)
            min_payment = min(payments)
            max_payment = max(payments)
            metrics.append(f'lyriq_payment_by_trim{{trim="{trim}"}} {avg_payment:.2f} {timestamp}')
            metrics.append(f'lyriq_payment_min_by_trim{{trim="{trim}"}} {min_payment} {timestamp}')
            metrics.append(f'lyriq_payment_max_by_trim{{trim="{trim}"}} {max_payment} {timestamp}')
    
    # Drive type by trim metrics
    drive_by_trim = defaultdict(lambda: defaultdict(int))
    for record in data:
        trim = record.get('trim', '')
        drive_type = record.get('drive_type', '')
        if trim and drive_type:
            clean_trim = trim.replace(' ', '_').replace('-', '_').lower()
            clean_drive = drive_type.replace(' ', '_').lower()
            drive_by_trim[clean_trim][clean_drive] += 1
    
    for trim, drives in drive_by_trim.items():
        for drive, count in drives.items():
            metrics.append(f'lyriq_vehicles_by_trim_drive{{trim="{trim}",drive_type="{drive}"}} {count} {timestamp}')
    
    # High-value vehicles (price > 50k)
    high_value_count = sum(1 for record in data if record.get('price', 0) > 50000)
    metrics.append(f"lyriq_high_value_vehicles {high_value_count} {timestamp}")
    
    # Low mileage vehicles (mileage < 5k)
    low_mileage_count = sum(1 for record in data if record.get('mileage', 0) < 5000 and record.get('mileage', 0) > 0)
    metrics.append(f"lyriq_low_mileage_vehicles {low_mileage_count} {timestamp}")
    
    # New vehicles (year 2025)
    new_vehicle_count = sum(1 for record in data if record.get('year', 0) == 2025)
    metrics.append(f"lyriq_new_vehicles {new_vehicle_count} {timestamp}")
    
    # AWD vs RWD ratio
    awd_count = sum(1 for record in data if record.get('drive_type', '').upper() == 'AWD')
    rwd_count = sum(1 for record in data if record.get('drive_type', '').upper() == 'RWD')
    if awd_count + rwd_count > 0:
        awd_ratio = awd_count / (awd_count + rwd_count)
        metrics.append(f"lyriq_awd_ratio {awd_ratio:.4f} {timestamp}")
    
    # Average age of vehicles (assuming current year 2025)
    current_year = 2025
    ages = [current_year - record.get('year', current_year) for record in data if record.get('year', 0) > 0]
    if ages:
        avg_age = sum(ages) / len(ages)
        metrics.append(f"lyriq_average_vehicle_age {avg_age:.2f} {timestamp}")
    
    # Price per mile ratio (for vehicles with both price and mileage)
    price_per_mile_data = []
    for record in data:
        price = record.get('price', 0)
        mileage = record.get('mileage', 0)
        if price > 0 and mileage > 0:
            price_per_mile_data.append(price / mileage)
    
    if price_per_mile_data:
        avg_price_per_mile = sum(price_per_mile_data) / len(price_per_mile_data)
        metrics.append(f"lyriq_average_price_per_mile {avg_price_per_mile:.2f} {timestamp}")
    
    # Write metrics to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# HELP lyriq_vehicles_total Total number of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_vehicles_total counter\n")
        f.write("# HELP lyriq_price_average Average price of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_price_average gauge\n")
        f.write("# HELP lyriq_price_min Minimum price of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_price_min gauge\n")
        f.write("# HELP lyriq_price_max Maximum price of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_price_max gauge\n")
        f.write("# HELP lyriq_mileage_average Average mileage of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_mileage_average gauge\n")
        f.write("# HELP lyriq_mileage_min Minimum mileage of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_mileage_min gauge\n")
        f.write("# HELP lyriq_mileage_max Maximum mileage of LYRIQ vehicles\n")
        f.write("# TYPE lyriq_mileage_max gauge\n")
        f.write("# HELP lyriq_vehicles_by_year Number of vehicles by year\n")
        f.write("# TYPE lyriq_vehicles_by_year gauge\n")
        f.write("# HELP lyriq_vehicles_by_trim Number of vehicles by trim\n")
        f.write("# TYPE lyriq_vehicles_by_trim gauge\n")
        f.write("# HELP lyriq_vehicles_by_state Number of vehicles by state\n")
        f.write("# TYPE lyriq_vehicles_by_state gauge\n")
        f.write("# HELP lyriq_vehicles_by_drive_type Number of vehicles by drive type\n")
        f.write("# TYPE lyriq_vehicles_by_drive_type gauge\n")
        f.write("# HELP lyriq_vehicles_by_interior_color Number of vehicles by interior color\n")
        f.write("# TYPE lyriq_vehicles_by_interior_color gauge\n")
        f.write("# HELP lyriq_vehicles_by_exterior_color Number of vehicles by exterior color\n")
        f.write("# TYPE lyriq_vehicles_by_exterior_color gauge\n")
        f.write("# HELP lyriq_vehicles_by_price_range Number of vehicles by price range\n")
        f.write("# TYPE lyriq_vehicles_by_price_range gauge\n")
        f.write("# HELP lyriq_vehicles_by_mileage_range Number of vehicles by mileage range\n")
        f.write("# TYPE lyriq_vehicles_by_mileage_range gauge\n")
        f.write("# HELP lyriq_payment_average Average payment amount\n")
        f.write("# TYPE lyriq_payment_average gauge\n")
        f.write("# HELP lyriq_payment_min Minimum payment amount\n")
        f.write("# TYPE lyriq_payment_min gauge\n")
        f.write("# HELP lyriq_payment_max Maximum payment amount\n")
        f.write("# TYPE lyriq_payment_max gauge\n")
        f.write("\n")
        
        for metric in metrics:
            f.write(metric + "\n")
    
    print(f"Generated {len(metrics)} Prometheus metrics")
    print(f"Metrics written to {output_file}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate Prometheus metrics from vehicle data")
    parser.add_argument("--input", "-i", default="cargurus-com-2025-10-02-final.json", 
                       help="Input JSON file (default: cargurus-com-2025-10-02-final.json)")
    parser.add_argument("--output", "-o", default="lyriq_metrics.prom", 
                       help="Output Prometheus metrics file (default: lyriq_metrics.prom)")
    parser.add_argument("--new-entries", action="store_true", 
                       help="Process new entries from 10-03 instead of main dataset")
    
    args = parser.parse_args()
    
    if args.new_entries:
        args.input = "new_entries_10_03.json"
        args.output = "lyriq_new_entries_metrics.prom"
    
    print(f"Generating Prometheus metrics from {args.input}")
    print("=" * 50)
    
    # Load data
    data = load_vehicle_data(args.input)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    print(f"Loaded {len(data)} vehicle records")
    
    # Generate metrics
    generate_prometheus_metrics(data, args.output)
    
    print(f"\nPrometheus metrics generated successfully!")
    print(f"File: {args.output}")
    print(f"Ready for Grafana Cloud ingestion")

if __name__ == "__main__":
    main()
