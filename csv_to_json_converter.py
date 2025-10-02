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
    python csv_to_json_converter.py input.csv [output.json] [options]

    # Examples:
    python csv_to_json_converter.py data.csv                    # Outputs to stdout
    python csv_to_json_converter.py data.csv output.json        # Outputs to file
    python csv_to_json_converter.py data.csv --stdout           # Force stdout output
    python csv_to_json_converter.py data.csv --duplicate-keys vin stock

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


def convert_drive_type(drive_type_str: str) -> str:
    """
    Convert drive type to abbreviated format.

    Examples:
        "All-Wheel Drive" → "AWD"
        "Rear-Wheel Drive" → "RWD"
        "" → ""
    """
    if not drive_type_str or drive_type_str.strip() == "":
        return ""

    drive_type_str = drive_type_str.strip()

    if "All-Wheel Drive" in drive_type_str:
        return "AWD"
    elif "Rear-Wheel Drive" in drive_type_str:
        return "RWD"
    else:
        return drive_type_str


def clean_trim_field(trim_str: str) -> str:
    """
    Remove AWD/RWD from trim field to avoid duplication with drive_type.

    Examples:
        "Tech AWD" → "Tech"
        "Luxury 3 AWD" → "Luxury 3"
        "Sport 1 RWD" → "Sport 1"
        "Tech" → "Tech"
    """
    if not trim_str or trim_str.strip() == "":
        return ""

    # Remove AWD and RWD from the end of trim strings
    cleaned = trim_str.strip()
    cleaned = re.sub(r"\s+AWD$", "", cleaned)
    cleaned = re.sub(r"\s+RWD$", "", cleaned)

    return cleaned


def is_empty_record(record: Dict[str, Any]) -> bool:
    """
    Check if a record is completely empty or has only empty values.

    Args:
        record (Dict): Record to check

    Returns:
        bool: True if record is empty, False otherwise
    """
    # Check if all values are empty strings, None, or missing
    for key, value in record.items():
        if value is not None and str(value).strip() != "":
            return False
    return True


def clean_record_data(
    record: Dict[str, Any], created_at_timestamp: str
) -> Dict[str, Any]:
    """
    Clean the record data by converting payment, price, mileage, and year to numbers.
    Also convert drive_type to abbreviations and clean trim field.
    Handle empty records, zero prices, missing mileage, and missing phone numbers.
    Add time timestamp to each record.

    Args:
        record (Dict): Record to clean
        created_at_timestamp (str): Timestamp to add to each record

    Returns:
        Dict: Cleaned record with time timestamp, or None if record should be removed
    """
    # Check if record is completely empty - remove it
    if is_empty_record(record):
        return None

    cleaned_record = record.copy()

    # Clean payment field
    if 'payment' in cleaned_record and cleaned_record['payment']:
        cleaned_record['payment'] = extract_payment_number(cleaned_record['payment'])
    else:
        cleaned_record["payment"] = 0

    # Clean price field - handle zero prices
    if 'price' in cleaned_record and cleaned_record['price']:
        price_value = extract_price_number(cleaned_record["price"])
        cleaned_record["price"] = price_value if price_value > 0 else 0
    else:
        cleaned_record["price"] = 0

    # Clean mileage field - handle missing mileage
    if 'milege' in cleaned_record and cleaned_record['milege']:
        mileage_value = extract_mileage_number(cleaned_record["milege"])
        cleaned_record["milege"] = mileage_value if mileage_value > 0 else 0
    else:
        cleaned_record["milege"] = 0

    # Clean year field
    if 'year' in cleaned_record and cleaned_record['year']:
        cleaned_record['year'] = extract_year_number(cleaned_record['year'])
    else:
        cleaned_record["year"] = 0

    # Handle missing phone numbers - set to default placeholder
    if "request_info" in cleaned_record:
        if (
            not cleaned_record["request_info"]
            or str(cleaned_record["request_info"]).strip() == ""
        ):
            cleaned_record["request_info"] = "(111) 111-1111"

    # Convert drive_type to abbreviations
    if "drive_type" in cleaned_record and cleaned_record["drive_type"]:
        cleaned_record["drive_type"] = convert_drive_type(cleaned_record["drive_type"])

    # Clean trim field (remove AWD/RWD to avoid duplication)
    if "trim" in cleaned_record and cleaned_record["trim"]:
        cleaned_record["trim"] = clean_trim_field(cleaned_record["trim"])

    # Handle LYRIQ-V model - set trim to V-Series
    if "model" in cleaned_record and cleaned_record["model"] == "LYRIQ-V":
        cleaned_record["trim"] = "V-Series"

    # Add time timestamp to each record
    cleaned_record["time"] = created_at_timestamp

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


def convert_csv_to_json(
    csv_file_path: str,
    json_file_path: str = None,
    duplicate_key_fields: List[str] = None,
    encoding: str = "utf-8",
    output_to_stdout: bool = False,
) -> Dict[str, Any]:
    """
    Convert CSV file to JSON format with normalization and deduplication.

    Args:
        csv_file_path (str): Path to input CSV file
        json_file_path (str): Path to output JSON file (None for stdout)
        duplicate_key_fields (List[str]): Fields to use for duplicate detection
        encoding (str): File encoding to use
        output_to_stdout (bool): Force output to stdout

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

            # Convert field names to normalized format and add time
            normalized_fieldnames = [
                normalize_field_name(field) for field in reader.fieldnames
            ] + ["time"]

            # Generate single timestamp for all records
            created_at_timestamp = datetime.now().isoformat()

            # Read all data
            data = []
            empty_records_removed = 0
            for row in reader:
                # Create new row with normalized field names
                normalized_row = {}
                for old_field, new_field in zip(
                    reader.fieldnames, normalized_fieldnames[:-1]
                ):  # Exclude time from field mapping
                    normalized_row[new_field] = row[old_field]

                # Clean the record data (convert payment, price, mileage to numbers)
                cleaned_row = clean_record_data(normalized_row, created_at_timestamp)

                # Only add non-empty records
                if cleaned_row is not None:
                    data.append(cleaned_row)
                else:
                    empty_records_removed += 1

        print(f"Read {len(data)} records from CSV file")
        if empty_records_removed > 0:
            print(f"Removed {empty_records_removed} empty records")

        # Remove duplicates
        original_count = len(data)
        data = remove_duplicates(data, duplicate_key_fields)
        duplicates_removed = original_count - len(data)

        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate records")

        # Create final JSON structure (just the data array)
        json_data = data

        # Determine output destination
        if output_to_stdout or json_file_path is None:
            # Output to stdout
            json.dump(json_data, sys.stdout, indent=2, ensure_ascii=False)
            print(
                f"\n# Conversion completed: {len(data)} records, {empty_records_removed} empty records removed, {duplicates_removed} duplicates removed",
                file=sys.stderr,
            )
        else:
            # Write to file
            with open(json_file_path, "w", encoding="utf-8") as jsonfile:
                json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)

            print(f"Successfully converted CSV to JSON: {json_file_path}")
            print(f"Total records: {len(data)}")
            print(f"Empty records removed: {empty_records_removed}")
            print(f"Duplicates removed: {duplicates_removed}")
            print("Data cleaning applied: payment, price, mileage, year → numbers")
            print("Drive type converted: All-Wheel Drive → AWD, Rear-Wheel Drive → RWD")
            print("Trim field cleaned: removed duplicate AWD/RWD references")
            print(
                "Data quality fixes: empty records removed, zero prices set to 0, missing mileage set to 0, missing phone numbers set to (111) 111-1111"
            )

        return {
            "success": True,
            "total_records": len(data),
            "empty_records_removed": empty_records_removed,
            "duplicates_removed": duplicates_removed,
            "output_file": json_file_path,
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
    parser.add_argument(
        "output_json",
        nargs="?",
        help="Path to output JSON file (if not specified, outputs to stdout)",
    )
    parser.add_argument("--duplicate-keys", nargs="+", 
                       help="Field names to use for duplicate detection (default: all fields)")
    parser.add_argument("--encoding", default="utf-8", 
                       help="File encoding (default: utf-8)")
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Force output to stdout (overrides output file)",
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_csv):
        print(f"Error: Input file '{args.input_csv}' does not exist")
        sys.exit(1)

    # Determine output behavior
    output_to_stdout = args.stdout or args.output_json is None

    # Perform conversion
    result = convert_csv_to_json(
        args.input_csv,
        args.output_json,
        args.duplicate_keys,
        args.encoding,
        output_to_stdout,
    )

    if result["success"]:
        print("Conversion completed successfully!")
        sys.exit(0)
    else:
        print(f"Conversion failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
