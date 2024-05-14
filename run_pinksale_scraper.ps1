# Set the execution policy for the current process to bypass restrictions
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Navigate to the directory
cd C:\Users\noush\OneDrive\Desktop\pinksale_scraper

# Set the environment variable for UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Activate the virtual environment
& .\venv\Scripts\Activate.ps1

# Function to run a Python script with color output
function Run-PythonScript {
    param (
        [string]$script
    )
    # Use Start-Process to run Python script in the current window and wait for completion
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList $script -Wait
}

# Start the first Python script as a job with color output
$job = Start-Job -ScriptBlock { Run-PythonScript "scrape_urls.py" }

# Wait for user input to stop the job
Write-Host "Press Enter to stop scrape_urls.py and start scrape_new.py"
Read-Host

# Stop the first job
Stop-Job $job
Receive-Job $job

# Run the second Python script with color output
Run-PythonScript "scrape_new.py"
