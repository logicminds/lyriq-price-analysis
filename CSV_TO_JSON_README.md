# CSV to JSON Converter

A Python script that converts CSV files to JSON format with field normalization, duplicate removal, and metadata tracking.

## Features

- **Field Name Normalization**: Converts field names to lowercase and replaces spaces with underscores
- **Duplicate Removal**: Removes duplicate entries based on specified key fields
- **Timestamp Tracking**: Adds conversion timestamp to the output
- **Metadata**: Includes comprehensive metadata about the conversion process
- **Flexible Duplicate Detection**: Choose which fields to use for duplicate detection
- **Encoding Support**: Handles different file encodings

## Usage

### Command Line

```bash
# Basic conversion
python csv_to_json_converter.py input.csv output.json

# With duplicate detection on specific fields
python csv_to_json_converter.py input.csv output.json --duplicate-keys vin stock

# With custom encoding
python csv_to_json_converter.py input.csv output.json --encoding utf-8
```

### Programmatic Usage

```python
from csv_to_json_converter import convert_csv_to_json

result = convert_csv_to_json(
    "input.csv", 
    "output.json", 
    duplicate_key_fields=["vin", "stock"]
)

if result["success"]:
    print(f"Converted {result['total_records']} records")
    print(f"Removed {result['duplicates_removed']} duplicates")
```

## Output Format

The JSON output includes:

```json
{
  "metadata": {
    "source_file": "input.csv",
    "conversion_timestamp": "2025-10-01T20:18:04.781887",
    "total_records": 609,
    "duplicates_removed": 144,
    "field_names": ["vin", "stock", "mileage", ...]
  },
  "data": [
    {
      "vin": "1GYKPMRL4RZ102008",
      "stock": "RZ102008",
      "mileage": "10,203",
      ...
    }
  ]
}
```

## Field Name Transformations

- `VIN` → `vin`
- `Stock` → `stock`
- `Interior Color` → `interior_color`
- `Exterior color` → `exterior_color`
- `Request Info` → `request_info`

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Examples

See `example_usage.py` for detailed usage examples.

## Recent Conversion Results

**Input**: `cargurus-com-2025-10-02.csv` (753 records)
**Output**: `cargurus-com-2025-02.json` (609 unique records)
**Duplicates Removed**: 144
**Key Fields Used**: `vin`, `stock`
