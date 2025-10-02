# Chart Data Extractor

This script extracts location and trim distribution data from the CarGurus JSON file and outputs it in the format needed for the index.html dashboard charts.

## Usage

### Basic Usage
```bash
python extract_chart_data.py
```
Uses default input file `cargurus-com-2025-10-02-final.json` and outputs to `chart_data.js`

### Custom Files
```bash
python extract_chart_data.py input.json output.js
```

### Output to Console
```bash
python extract_chart_data.py --stdout
```

## Output

The script generates JavaScript objects that can be directly copied into the index.html file:

1. **locationData** - Geographic distribution with vehicle counts, average prices, and top trims per state
2. **trimDistributionData** - Trim level distribution across states for the stacked bar chart
3. **trimColors** - Color palette for different trim levels

## Features

- **Automatic Data Processing**: Extracts state information from location strings
- **Statistical Analysis**: Calculates average prices and trim preferences per state
- **Data Filtering**: Only includes states with 5+ vehicles in trim distribution chart
- **Summary Statistics**: Provides overview of data processing results
- **Error Handling**: Validates JSON format and file existence

## Generated Data Structure

### Location Data
```javascript
const locationData = {
    'CA': { count: 82, avgPrice: 53484, trims: ['Sport 1', 'Luxury 1', 'Luxury 2'] },
    'TX': { count: 62, avgPrice: 44142, trims: ['Luxury 3', 'Luxury 1', 'Sport 3'] },
    // ... more states
};
```

### Trim Distribution Data
```javascript
const trimDistributionData = {
    trims: ['Luxury', 'Luxury 1', 'Luxury 2', 'Luxury 3', 'Sport 1', 'Sport 2', 'Sport 3', 'Tech', 'V-Series'],
    states: [
        { state: 'CA', total: 82, trims: [3, 24, 7, 4, 28, 7, 5, 4, 0] },
        // ... more states
    ]
};
```

### Color Palette
```javascript
const trimColors = {
    'Luxury': '#4ECDC4',
    'Luxury 1': '#45B7D1',
    'Luxury 2': '#96CEB4',
    'Luxury 3': '#FFEAA7',
    'Sport 1': '#DDA0DD',
    'Sport 2': '#98D8C8',
    'Sport 3': '#F7DC6F',
    'Tech': '#BB8FCE',
    'V-Series': '#FF6B6B'
};
```

## Integration with Dashboard

1. Run the script to generate updated chart data
2. Copy the generated JavaScript objects into index.html
3. Update chart titles with current date if needed
4. Test the dashboard to ensure charts display correctly

## Requirements

- Python 3.6+
- JSON file with vehicle data in the expected format
- No additional dependencies required

## Example Output

The script provides summary statistics including:
- Total records processed
- Number of states with data
- Unique trim levels found
- Top 5 states by inventory
- Trim level distribution percentages
