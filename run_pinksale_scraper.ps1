# Set the execution policy for the current process to bypass restrictions
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Determine the script's directory
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# Navigate to the script's directory
Set-Location $scriptDir

# Activate the virtual environment
& .\venv\Scripts\Activate.ps1

# Verify that the virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Failed to activate virtual environment. Exiting."
    exit 1
}

# Prompt user for the weeks to process (comma-separated)
$includeWeeks = Read-Host "Enter the weeks you want to process, comma separated"

# Function to clean up background job
function Cleanup {
    if ($global:job -and $global:job.State -eq 'Running') {
        Stop-Job -Id $global:job.Id
        Remove-Job -Id $global:job.Id
    }
}

# Set trap to clean up background job on exit
Register-EngineEvent PowerShell.Exiting -Action { Cleanup }

# Run the first Python script in the background
$global:job = Start-Job -ScriptBlock {
    param($weeks)
    & python scrape_urls.py $weeks
} -ArgumentList $includeWeeks

# Wait for user input to stop the job
Write-Host "Press Enter to stop scrape_urls.py and start scrape_new.py"
Read-Host

# Stop the first job
Cleanup

# Run the second Python script
& python scrape_new.py
