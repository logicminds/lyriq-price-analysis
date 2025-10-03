#!/usr/bin/env python3
"""
HTTP server to serve Prometheus metrics for LYRIQ vehicle data.
This allows Prometheus to scrape the metrics via HTTP endpoint.
"""

import os
import time
import argparse
from flask import Flask, Response
from generate_prometheus_metrics import load_vehicle_data, generate_prometheus_metrics
import tempfile

app = Flask(__name__)

# Global variables for metrics
metrics_data = None
last_update = 0
update_interval = 300  # 5 minutes

def update_metrics(json_file: str):
    """Update metrics data from JSON file."""
    global metrics_data, last_update
    
    current_time = time.time()
    if current_time - last_update < update_interval and metrics_data is not None:
        return metrics_data
    
    print(f"Updating metrics from {json_file}")
    data = load_vehicle_data(json_file)
    
    if not data:
        return None
    
    # Generate metrics to temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.prom') as temp_file:
        generate_prometheus_metrics(data, temp_file.name)
        
        # Read the generated metrics
        with open(temp_file.name, 'r') as f:
            metrics_data = f.read()
        
        # Clean up temp file
        os.unlink(temp_file.name)
    
    last_update = current_time
    return metrics_data

@app.route('/metrics')
def metrics():
    """Serve Prometheus metrics."""
    global metrics_data
    
    if metrics_data is None:
        return "No metrics available", 503
    
    return Response(metrics_data, mimetype='text/plain')

@app.route('/health')
def health():
    """Health check endpoint."""
    return {"status": "healthy", "last_update": last_update}

@app.route('/reload')
def reload():
    """Force reload of metrics."""
    global metrics_data, last_update
    metrics_data = None
    last_update = 0
    return {"status": "reload_triggered"}

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="HTTP server for LYRIQ Prometheus metrics")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to run server on (default: 8080)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--input", "-i", default="cargurus-com-2025-10-02-final.json", 
                       help="Input JSON file (default: cargurus-com-2025-10-02-final.json)")
    parser.add_argument("--new-entries", action="store_true", 
                       help="Serve new entries metrics instead of main dataset")
    parser.add_argument("--interval", type=int, default=300, 
                       help="Update interval in seconds (default: 300)")
    
    args = parser.parse_args()
    
    global update_interval
    update_interval = args.interval
    
    if args.new_entries:
        args.input = "new_entries_10_03.json"
    
    print(f"Starting metrics server on {args.host}:{args.port}")
    print(f"Input file: {args.input}")
    print(f"Update interval: {args.interval} seconds")
    print("=" * 50)
    
    # Initial metrics load
    update_metrics(args.input)
    
    if metrics_data is None:
        print("Failed to load initial metrics. Exiting.")
        return
    
    print("Metrics server ready!")
    print(f"Metrics endpoint: http://{args.host}:{args.port}/metrics")
    print(f"Health check: http://{args.host}:{args.port}/health")
    print(f"Force reload: http://{args.host}:{args.port}/reload")
    
    # Start the Flask app
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
