#!/bin/bash

# Exit on any error
set -e

# Step 1: Remove existing virtual environment if it exists
if [ -d "venv" ]; then
  echo "🧹 Removing existing virtual environment..."
  rm -rf venv
else
  echo "✅ No existing virtual environment found."
fi

# Step 2: Create new virtual environment
echo "🐍 Creating new virtual environment..."
python3 -m venv venv

# Step 3: Activate the virtual environment
echo "🔁 Activating virtual environment..."
source venv/bin/activate

# Step 4: Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

chmod +x snake

echo "✅ Setup complete. Virtual environment is active."