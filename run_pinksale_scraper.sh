#!/bin/bash

# Determine the script's directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Navigate to the script's directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source venv/bin/activate

# Verify that the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Failed to activate virtual environment. Exiting."
    exit 1
fi

# Prompt user for the number of weeks to process
read -p "Enter the weeks you want to process, comma separated: " include_weeks

# Function to clean up background job
cleanup() {
    if [ -n "$pid" ]; then
        kill $pid
    fi
}

# Set trap to clean up background job on exit
trap cleanup EXIT

# Run the first Python script in the background
python scrape_urls.py "$include_weeks" &

# Get the PID of the background job
pid=$!

# Wait for user input to stop the first script
read -p "Press Enter to stop scrape_urls.py and start scrape_new.py"

# Kill the first Python script
cleanup

# Run the second Python script
python scrape_new.py
