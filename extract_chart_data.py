#!/usr/bin/env python3
"""
Chart Data Extractor for Cadillac Lyriq Dashboard

This script extracts location and trim distribution data from the CarGurus JSON file
and outputs it in the format needed for the index.html dashboard charts.

Usage:
    python extract_chart_data.py [input_json] [output_file]

Examples:
    python extract_chart_data.py cargurus-com-2025-10-02-final.json chart_data.js
    python extract_chart_data.py  # Uses default files
"""

import json
import sys
import argparse
from collections import defaultdict, Counter
from typing import Dict, List, Any


def extract_location_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract location-based data for the geographic distribution chart.
    
    Args:
        data: List of vehicle records from JSON
        
    Returns:
        Dictionary with location data formatted for JavaScript
    """
    state_data = defaultdict(lambda: {'count': 0, 'prices': [], 'trims': []})
    
    for record in data:
        location = record.get('location', '')
        if location:
            # Extract state from location (assuming format is 'City, ST')
            if ', ' in location:
                state = location.split(', ')[-1]
            else:
                state = location
            
            price = record.get('price', 0)
            trim = record.get('trim', '')
            
            state_data[state]['count'] += 1
            if price > 0:  # Only include non-zero prices
                state_data[state]['prices'].append(price)
            if trim:
                state_data[state]['trims'].append(trim)
    
    # Calculate statistics and format for JavaScript
    result = {}
    for state, data in state_data.items():
        if data['count'] > 0:
            avg_price = sum(data['prices']) / len(data['prices']) if data['prices'] else 0
            trim_counts = Counter(data['trims'])
            top_trims = [trim for trim, count in trim_counts.most_common(3)]
            
            result[state] = {
                'count': data['count'],
                'avgPrice': int(avg_price),
                'trims': top_trims
            }
    
    # Sort by count (descending)
    sorted_states = sorted(result.items(), key=lambda x: x[1]['count'], reverse=True)
    
    return sorted_states


def extract_trim_distribution_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract trim distribution data for the stacked bar chart.
    
    Args:
        data: List of vehicle records from JSON
        
    Returns:
        Dictionary with trim distribution data formatted for JavaScript
    """
    trim_by_state = defaultdict(lambda: defaultdict(int))
    state_totals = defaultdict(int)
    
    for record in data:
        location = record.get('location', '')
        trim = record.get('trim', '')
        
        if location and trim:
            # Extract state from location
            if ', ' in location:
                state = location.split(', ')[-1]
            else:
                state = location
            
            trim_by_state[state][trim] += 1
            state_totals[state] += 1
    
    # Get all unique trims
    all_trims = set()
    for state_data in trim_by_state.values():
        all_trims.update(state_data.keys())
    
    all_trims = sorted(list(all_trims))
    
    # Prepare data for JavaScript
    states_data = []
    sorted_states = sorted(state_totals.items(), key=lambda x: x[1], reverse=True)
    
    for state, total in sorted_states:
        if total >= 5:  # Only include states with 5+ vehicles
            trim_counts = []
            for trim in all_trims:
                count = trim_by_state[state].get(trim, 0)
                trim_counts.append(count)
            
            states_data.append({
                'state': state,
                'total': total,
                'trims': trim_counts
            })
    
    return {
        'trims': all_trims,
        'states': states_data
    }


def format_location_data_js(location_data: List[tuple]) -> str:
    """
    Format location data as JavaScript object.
    
    Args:
        location_data: List of (state, data) tuples
        
    Returns:
        JavaScript object string
    """
    js_lines = ['// Location data for geographic distribution chart', 'const locationData = {']
    
    for i, (state, data) in enumerate(location_data):
        comma = ',' if i < len(location_data) - 1 else ''
        js_lines.append(f"    '{state}': {{ count: {data['count']}, avgPrice: {data['avgPrice']}, trims: {data['trims']} }}{comma}")
    
    js_lines.append('};')
    return '\n'.join(js_lines)


def format_trim_distribution_data_js(trim_data: Dict[str, Any]) -> str:
    """
    Format trim distribution data as JavaScript object.
    
    Args:
        trim_data: Dictionary with trim distribution data
        
    Returns:
        JavaScript object string
    """
    js_lines = ['// Trim distribution data for stacked bar chart', 'const trimDistributionData = {']
    js_lines.append(f"    trims: {trim_data['trims']},")
    js_lines.append('    states: [')
    
    for i, state_data in enumerate(trim_data['states']):
        comma = ',' if i < len(trim_data['states']) - 1 else ''
        js_lines.append(f"        {{ state: '{state_data['state']}', total: {state_data['total']}, trims: {state_data['trims']} }}{comma}")
    
    js_lines.append('    ]')
    js_lines.append('};')
    return '\n'.join(js_lines)


def generate_color_palette_js(trims: List[str]) -> str:
    """
    Generate JavaScript color palette for trims.
    
    Args:
        trims: List of trim names
        
    Returns:
        JavaScript color palette object
    """
    # Color palette for trims
    color_mapping = {
        'Luxury': '#4ECDC4',
        'Luxury 1': '#45B7D1',
        'Luxury 2': '#96CEB4',
        'Luxury 3': '#FFEAA7',
        'Sport 1': '#DDA0DD',
        'Sport 2': '#98D8C8',
        'Sport 3': '#F7DC6F',
        'Tech': '#BB8FCE',
        'V-Series': '#FF6B6B'
    }
    
    js_lines = ['// Color palette for trim levels', 'const trimColors = {']
    
    for i, trim in enumerate(trims):
        color = color_mapping.get(trim, '#CCCCCC')  # Default gray for unknown trims
        comma = ',' if i < len(trims) - 1 else ''
        js_lines.append(f"    '{trim}': '{color}'{comma}")
    
    js_lines.append('};')
    return '\n'.join(js_lines)


def main():
    """Main function to extract chart data from JSON file."""
    parser = argparse.ArgumentParser(
        description="Extract chart data from CarGurus JSON file for dashboard"
    )
    parser.add_argument(
        "input_json",
        nargs="?",
        default="cargurus-com-2025-10-02-final.json",
        help="Path to input JSON file (default: cargurus-com-2025-10-02-final.json)"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="chart_data.js",
        help="Path to output JavaScript file (default: chart_data.js)"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Output to stdout instead of file"
    )
    
    args = parser.parse_args()
    
    try:
        # Load JSON data
        print(f"Loading data from {args.input_json}...")
        with open(args.input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Processing {len(data)} records...")
        
        # Extract location data
        print("Extracting location data...")
        location_data = extract_location_data(data)
        
        # Extract trim distribution data
        print("Extracting trim distribution data...")
        trim_data = extract_trim_distribution_data(data)
        
        # Generate JavaScript output
        print("Generating JavaScript output...")
        output_lines = []
        
        # Add header comment
        output_lines.append("// Auto-generated chart data for Cadillac Lyriq Dashboard")
        output_lines.append("// Generated from CarGurus JSON data")
        output_lines.append("// Do not edit manually - regenerate using extract_chart_data.py")
        output_lines.append("")
        
        # Add location data
        output_lines.append(format_location_data_js(location_data))
        output_lines.append("")
        
        # Add trim distribution data
        output_lines.append(format_trim_distribution_data_js(trim_data))
        output_lines.append("")
        
        # Add color palette
        output_lines.append(generate_color_palette_js(trim_data['trims']))
        output_lines.append("")
        
        # Add usage instructions
        output_lines.append("// Usage instructions:")
        output_lines.append("// 1. Copy the locationData object to replace the locationData in index.html")
        output_lines.append("// 2. Copy the trimDistributionData object to replace the trimDistributionData in index.html")
        output_lines.append("// 3. Copy the trimColors object to replace the trimColors in index.html")
        output_lines.append("// 4. Update chart titles with current date if needed")
        
        # Output results
        output_content = '\n'.join(output_lines)
        
        if args.stdout:
            print("\n" + "="*60)
            print("CHART DATA OUTPUT")
            print("="*60)
            print(output_content)
        else:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Chart data written to {args.output_file}")
        
        # Print summary statistics
        print(f"\nSummary:")
        print(f"  Total records processed: {len(data)}")
        print(f"  States with data: {len(location_data)}")
        print(f"  Unique trim levels: {len(trim_data['trims'])}")
        print(f"  States in trim chart: {len(trim_data['states'])}")
        
        # Show top states by inventory
        print(f"\nTop 5 states by inventory:")
        for i, (state, data) in enumerate(location_data[:5]):
            print(f"  {i+1}. {state}: {data['count']} vehicles (avg: ${data['avgPrice']:,})")
        
        # Show trim distribution
        print(f"\nTrim level distribution:")
        trim_counts = Counter()
        for record in data:
            if isinstance(record, dict):
                trim = record.get('trim', '')
                if trim:
                    trim_counts[trim] += 1
        
        for trim, count in trim_counts.most_common():
            percentage = (count / len(data)) * 100
            print(f"  {trim}: {count} vehicles ({percentage:.1f}%)")
        
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_json}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{args.input_json}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
