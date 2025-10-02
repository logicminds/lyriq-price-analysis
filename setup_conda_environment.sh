#!/bin/bash
"""
Setup script for CarGurus LYRIQ conda environment
"""

echo "🚀 Setting up CarGurus LYRIQ environment..."
echo "=" * 60

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Anaconda or Miniconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda found"

# Create the environment from the yml file
echo "📦 Creating conda environment from environment.yml..."
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo "✅ Environment created successfully"
else
    echo "❌ Failed to create environment"
    exit 1
fi

# Activate the environment
echo "🔄 Activating environment..."
conda activate lyriq-price

if [ $? -eq 0 ]; then
    echo "✅ Environment activated"
else
    echo "❌ Failed to activate environment"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo "=" * 60
echo "📋 To use the environment:"
echo "   conda activate lyriq-price"
echo ""
