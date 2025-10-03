# LYRIQ Vehicle Data - Prometheus Metrics for Grafana Cloud

This document describes how to use the generated Prometheus metrics with Grafana Cloud for monitoring and visualizing LYRIQ vehicle inventory data.

## Generated Metrics Files

- `lyriq_metrics.prom` - Main dataset metrics (623 vehicles)
- `lyriq_new_entries_metrics.prom` - New entries metrics (30 vehicles)

## Available Metrics

### Core Metrics
- `lyriq_vehicles_total` - Total number of vehicles
- `lyriq_price_average` - Average vehicle price
- `lyriq_price_min` - Minimum vehicle price  
- `lyriq_price_max` - Maximum vehicle price
- `lyriq_mileage_average` - Average vehicle mileage
- `lyriq_mileage_min` - Minimum vehicle mileage
- `lyriq_mileage_max` - Maximum vehicle mileage
- `lyriq_payment_average` - Average monthly payment
- `lyriq_payment_min` - Minimum monthly payment
- `lyriq_payment_max` - Maximum monthly payment

### Distribution Metrics
- `lyriq_vehicles_by_year{year="2024"}` - Vehicles by year
- `lyriq_vehicles_by_trim{trim="luxury_3"}` - Vehicles by trim level
- `lyriq_vehicles_by_state{state="california"}` - Vehicles by state
- `lyriq_vehicles_by_drive_type{drive_type="awd"}` - Vehicles by drive type
- `lyriq_vehicles_by_interior_color{color="noir"}` - Vehicles by interior color
- `lyriq_vehicles_by_exterior_color{color="stellar_black"}` - Vehicles by exterior color

### Range Metrics
- `lyriq_vehicles_by_price_range{range="under_40k"}` - Vehicles by price range
- `lyriq_vehicles_by_mileage_range{range="under_10k"}` - Vehicles by mileage range

## Usage with Grafana Cloud

### 1. Set up Prometheus Data Source

1. In Grafana Cloud, go to **Configuration** → **Data Sources**
2. Add a new **Prometheus** data source
3. Configure the URL to point to your Prometheus instance
4. Test the connection

### 2. Import Metrics

You can use these metrics in several ways:

#### Option A: Direct File Import
```bash
# Copy metrics to your Prometheus server
scp lyriq_metrics.prom user@prometheus-server:/var/lib/prometheus/
```

#### Option B: HTTP Endpoint
Set up an HTTP endpoint that serves the metrics:
```python
from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    with open('lyriq_metrics.prom', 'r') as f:
        return Response(f.read(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### 3. Sample Grafana Queries

#### Vehicle Count by Year
```promql
lyriq_vehicles_by_year
```

#### Price Distribution
```promql
lyriq_vehicles_by_price_range
```

#### Average Price Over Time
```promql
lyriq_price_average
```

#### Top States by Vehicle Count
```promql
topk(10, lyriq_vehicles_by_state)
```

#### Trim Level Distribution
```promql
lyriq_vehicles_by_trim
```

### 4. Sample Dashboard Panels

#### Single Stat Panels
- **Total Vehicles**: `lyriq_vehicles_total`
- **Average Price**: `lyriq_price_average`
- **Average Mileage**: `lyriq_mileage_average`

#### Bar Charts
- **Vehicles by Year**: `lyriq_vehicles_by_year`
- **Vehicles by Trim**: `lyriq_vehicles_by_trim`
- **Vehicles by State**: `lyriq_vehicles_by_state`

#### Pie Charts
- **Price Range Distribution**: `lyriq_vehicles_by_price_range`
- **Mileage Range Distribution**: `lyriq_vehicles_by_mileage_range`

### 5. Alerting Rules

#### High Price Alert
```yaml
- alert: HighAveragePrice
  expr: lyriq_price_average > 50000
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Average LYRIQ price is above $50,000"
```

#### Low Inventory Alert
```yaml
- alert: LowInventory
  expr: lyriq_vehicles_total < 100
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "LYRIQ inventory is below 100 vehicles"
```

## Automation

### Generate Metrics Automatically
```bash
# Add to crontab for daily updates
0 6 * * * cd /path/to/lyriq-price && python generate_prometheus_metrics.py
```

### Update New Entries
```bash
# Generate metrics for new entries
python generate_prometheus_metrics.py --new-entries
```

## File Structure

```
lyriq-price/
├── generate_prometheus_metrics.py    # Script to generate metrics
├── lyriq_metrics.prom               # Main dataset metrics
├── lyriq_new_entries_metrics.prom   # New entries metrics
├── cargurus-com-2025-10-02-final.json  # Source data
└── new_entries_10_03.json           # New entries data
```

## Metric Naming Convention

All metrics follow the `lyriq_` prefix for easy identification:
- `lyriq_vehicles_*` - Vehicle count metrics
- `lyriq_price_*` - Price-related metrics
- `lyriq_mileage_*` - Mileage-related metrics
- `lyriq_payment_*` - Payment-related metrics

## Labels

Metrics use consistent label naming:
- `year` - Vehicle year (2023, 2024, 2025)
- `trim` - Trim level (luxury_3, sport_1, etc.)
- `state` - US state (california, texas, etc.)
- `drive_type` - Drive type (awd, rwd)
- `color` - Color (stellar_black, etc.)
- `range` - Price/mileage ranges

## Next Steps

1. Set up Prometheus to scrape these metrics
2. Create Grafana dashboards using the provided queries
3. Set up alerting rules for business-critical thresholds
4. Automate metric generation with cron jobs
5. Monitor trends over time to identify market patterns
