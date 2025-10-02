#!/usr/bin/env python3
"""
Example usage of the CSV to JSON converter script.

This demonstrates how to use the csv_to_json_converter.py script
programmatically or from the command line.
"""

import subprocess
import sys
import os
from csv_to_json_converter import convert_csv_to_json


def example_command_line_usage():
    """Example of using the converter from command line."""
    print("=== Command Line Usage Examples ===")
    print()
    print("Basic conversion (outputs to stdout):")
    print("python csv_to_json_converter.py input.csv")
    print()
    print("Output to file:")
    print("python csv_to_json_converter.py input.csv output.json")
    print()
    print("Force stdout output:")
    print("python csv_to_json_converter.py input.csv output.json --stdout")
    print()
    print("With duplicate detection on specific fields:")
    print("python csv_to_json_converter.py input.csv --duplicate-keys vin stock")
    print()
    print("With custom encoding:")
    print("python csv_to_json_converter.py input.csv --encoding utf-8")
    print()


def example_programmatic_usage():
    """Example of using the converter programmatically."""
    print("=== Programmatic Usage Example ===")
    print()
    
    # Example: Convert a CSV file programmatically
    csv_file = "cargurus-com-2025-10-02.csv"
    json_file = "example_output.json"
    
    if os.path.exists(csv_file):
        result = convert_csv_to_json(
            csv_file, 
            json_file, 
            duplicate_key_fields=["vin", "stock"]
        )
        
        if result["success"]:
            print(f"✅ Conversion successful!")
            print(f"   Total records: {result['total_records']}")
            print(f"   Duplicates removed: {result['duplicates_removed']}")
            print(f"   Output file: {result['output_file']}")
        else:
            print(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Input file '{csv_file}' not found")


def run_conversion_example():
    """Run the actual conversion as an example."""
    print("=== Running Conversion Example ===")
    print()
    
    # Run the conversion
    cmd = [
        sys.executable, 
        "csv_to_json_converter.py", 
        "cargurus-com-2025-10-02.csv", 
        "cargurus-com-2025-10-02.json",
        "--duplicate-keys", "vin", "stock"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Conversion completed successfully!")
        print("Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Conversion failed!")
        print("Error output:")
        print(e.stderr)
    except FileNotFoundError:
        print("❌ Python interpreter not found")


if __name__ == "__main__":
    print("CSV to JSON Converter - Usage Examples")
    print("=" * 50)
    print()
    
    example_command_line_usage()
    example_programmatic_usage()
    
    # Uncomment the line below to run an actual conversion example
    # run_conversion_example()
