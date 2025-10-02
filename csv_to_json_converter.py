#!/usr/bin/env python3
"""
CSV to JSON Converter Script

This script converts CSV files to JSON format with the following transformations:
- Converts field names to lowercase
- Replaces spaces with underscores in field names
- Removes duplicate entries
- Adds a timestamp of when the data was parsed
- Handles various CSV formats and edge cases

Usage:
    python csv_to_json_converter.py input.csv output.json

Author: Generated for lyriq-price project
"""

import csv
import json
import sys
import argparse
import re
from datetime import datetime
from typing import List, Dict, Any
import os


def normalize_field_name(field_name: str) -> str:
    """
    Normalize field names by converting to lowercase and replacing spaces with underscores.
    
    Args:
        field_name (str): Original field name
        
    Returns:
        str: Normalized field name
    """
    return field_name.lower().replace(' ', '_').replace('-', '_')


def extract_payment_number(payment_str: str) -> int:
    """
    Extract the numeric value from payment string.
    
    Examples:
        "$670/mo est." → 670
        "$1,068/mo est." → 1068
        "" → 0
    """
    if not payment_str or payment_str.strip() == "":
        return 0
    
    # Remove all non-numeric characters except commas and periods
    cleaned = re.sub(r'[^\d,.]', '', payment_str)
    
    # Remove commas and convert to int
    try:
        return int(float(cleaned.replace(',', '')))
    except (ValueError, TypeError):
        return 0


def extract_price_number(price_str: str) -> int:
    """
    Extract the numeric value from price string.
    
    Examples:
        "$37,900.00" → 37900
        "$44,468.00" → 44468
        "" → 0
    """
    if not price_str or price_str.strip() == "":
        return 0
    
    # Remove all non-numeric characters except commas and periods
    cleaned = re.sub(r'[^\d,.]', '', price_str)
    
    # Remove commas and convert to int
    try:
        return int(float(cleaned.replace(',', '')))
    except (ValueError, TypeError):
        return 0


def extract_mileage_number(mileage_str: str) -> int:
    """
    Extract the numeric value from mileage string.
    
    Examples:
        "10,203" → 10203
        "357" → 357
        "" → 0
    """
    if not mileage_str or mileage_str.strip() == "":
        return 0
    
    # Remove all non-numeric characters except commas
    cleaned = re.sub(r'[^\d,]', '', mileage_str)
    
    # Remove commas and convert to int
    try:
        return int(cleaned.replace(',', ''))
    except (ValueError, TypeError):
        return 0


def extract_year_number(year_str: str) -> int:
    """
    Extract the numeric value from year string.
    
    Examples:
        "2024" → 2024
        "2025" → 2025
        "" → 0
    """
    if not year_str or year_str.strip() == "":
        return 0

    # Remove all non-numeric characters
    cleaned = re.sub(r'[^\d]', '', year_str)

    # Convert to int
    try:
        return int(cleaned)
    except (ValueError, TypeError):
        return 0


def clean_record_data(
    record: Dict[str, Any], created_at_timestamp: str
) -> Dict[str, Any]:
    """
    Clean the record data by converting payment, price, mileage, and year to numbers.
    Also add created_at timestamp to each record.

    Args:
        record (Dict): Record to clean
        created_at_timestamp (str): Timestamp to add to each record

    Returns:
        Dict: Cleaned record with created_at timestamp
    """
    cleaned_record = record.copy()

    # Clean payment field
    if 'payment' in cleaned_record and cleaned_record['payment']:
        cleaned_record['payment'] = extract_payment_number(cleaned_record['payment'])

    # Clean price field
    if 'price' in cleaned_record and cleaned_record['price']:
        cleaned_record['price'] = extract_price_number(cleaned_record['price'])

    # Clean mileage field
    if 'milege' in cleaned_record and cleaned_record['milege']:
        cleaned_record['milege'] = extract_mileage_number(cleaned_record['milege'])

    # Clean year field
    if 'year' in cleaned_record and cleaned_record['year']:
        cleaned_record['year'] = extract_year_number(cleaned_record['year'])

    # Add created_at timestamp to each record
    cleaned_record["created_at"] = created_at_timestamp

    return cleaned_record


def remove_duplicates(data: List[Dict[str, Any]], key_fields: List[str] = None) -> List[Dict[str, Any]]:
    """
    Remove duplicate entries from the data.
    
    Args:
        data (List[Dict]): List of dictionaries containing the data
        key_fields (List[str]): Fields to use for duplicate detection. If None, uses all fields.
        
    Returns:
        List[Dict]: Data with duplicates removed
    """
    if not data:
        return data
    
    if key_fields is None:
        # Use all fields for duplicate detection
        key_fields = list(data[0].keys())
    
    seen = set()
    unique_data = []
    
    for record in data:
        # Create a key based on the specified fields
        key_parts = []
        for field in key_fields:
            if field in record:
                key_parts.append(str(record[field]))
            else:
                key_parts.append('')
        key = '|'.join(key_parts)
        
        if key not in seen:
            seen.add(key)
            unique_data.append(record)
    
    return unique_data


def convert_csv_to_json(csv_file_path: str, json_file_path: str, 
                       duplicate_key_fields: List[str] = None,
                       encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Convert CSV file to JSON format with normalization and deduplication.
    
    Args:
        csv_file_path (str): Path to input CSV file
        json_file_path (str): Path to output JSON file
        duplicate_key_fields (List[str]): Fields to use for duplicate detection
        encoding (str): File encoding to use
        
    Returns:
        Dict: Summary of conversion process
    """
    try:
        # Read CSV file
        with open(csv_file_path, 'r', encoding=encoding, newline='') as csvfile:
            # Detect delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter

            reader = csv.DictReader(csvfile, delimiter=delimiter)

            # Convert field names to normalized format and add created_at
            normalized_fieldnames = [
                normalize_field_name(field) for field in reader.fieldnames
            ] + ["created_at"]

            # Generate single timestamp for all records
            created_at_timestamp = datetime.now().isoformat()

            # Read all data
            data = []
            for row in reader:
                # Create new row with normalized field names
                normalized_row = {}
                for old_field, new_field in zip(
                    reader.fieldnames, normalized_fieldnames[:-1]
                ):  # Exclude created_at from field mapping
                    normalized_row[new_field] = row[old_field]

                # Clean the record data (convert payment, price, mileage to numbers)
                cleaned_row = clean_record_data(normalized_row, created_at_timestamp)
                data.append(cleaned_row)

        print(f"Read {len(data)} records from CSV file")

        # Remove duplicates
        original_count = len(data)
        data = remove_duplicates(data, duplicate_key_fields)
        duplicates_removed = original_count - len(data)

        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate records")

        # Add timestamp
        timestamp = datetime.now().isoformat()

        # Count data cleaning conversions
        payment_conversions = sum(1 for record in data if isinstance(record.get('payment'), int) and record.get('payment', 0) > 0)
        price_conversions = sum(1 for record in data if isinstance(record.get('price'), int) and record.get('price', 0) > 0)
        mileage_conversions = sum(1 for record in data if isinstance(record.get('milege'), int) and record.get('milege', 0) > 0)
        year_conversions = sum(1 for record in data if isinstance(record.get('year'), int) and record.get('year', 0) > 0)

        # Create final JSON structure
        json_data = {
            "metadata": {
                "source_file": os.path.basename(csv_file_path),
                "conversion_timestamp": timestamp,
                "total_records": len(data),
                "duplicates_removed": duplicates_removed,
                "field_names": normalized_fieldnames,
                "data_cleaning": {
                    "payment_conversions": payment_conversions,
                    "price_conversions": price_conversions,
                    "mileage_conversions": mileage_conversions,
                    "year_conversions": year_conversions,
                    "description": "Payment, price, mileage, and year fields converted to numeric values"
                }
            },
            "data": data
        }

        # Write JSON file
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)

        print(f"Successfully converted CSV to JSON: {json_file_path}")
        print(f"Total records: {len(data)}")
        print(f"Duplicates removed: {duplicates_removed}")
        print(f"Payment conversions: {payment_conversions}")
        print(f"Price conversions: {price_conversions}")
        print(f"Mileage conversions: {mileage_conversions}")
        print(f"Year conversions: {year_conversions}")

        return {
            "success": True,
            "total_records": len(data),
            "duplicates_removed": duplicates_removed,
            "output_file": json_file_path
        }

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found")
        return {"success": False, "error": "File not found"}
    except Exception as e:
        print(f"Error converting CSV to JSON: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Main function to handle command line arguments and execute conversion."""
    parser = argparse.ArgumentParser(
        description="Convert CSV file to JSON format with field normalization and deduplication"
    )
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("output_json", help="Path to output JSON file")
    parser.add_argument("--duplicate-keys", nargs="+", 
                       help="Field names to use for duplicate detection (default: all fields)")
    parser.add_argument("--encoding", default="utf-8", 
                       help="File encoding (default: utf-8)")
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_csv):
        print(f"Error: Input file '{args.input_csv}' does not exist")
        sys.exit(1)
    
    # Perform conversion
    result = convert_csv_to_json(
        args.input_csv, 
        args.output_json, 
        args.duplicate_keys,
        args.encoding
    )
    
    if result["success"]:
        print("Conversion completed successfully!")
        sys.exit(0)
    else:
        print(f"Conversion failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
