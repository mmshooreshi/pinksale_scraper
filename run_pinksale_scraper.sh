#!/bin/bash

# Navigate to the directory
cd ~/OneDrive/Desktop/pinksale_scraper

# Activate the virtual environment
source venv/bin/activate

# Run the first Python script in the background
python scrape_urls.py &

# Get the PID of the background job
pid=$!

# Wait for user input to stop the first script
read -p "Press Enter to stop scrape_urls.py and start scrape_new.py"

# Kill the first Python script
kill $pid

# Run the second Python script
python scrape_new.py
