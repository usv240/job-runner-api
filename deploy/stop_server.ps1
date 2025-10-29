Write-Host "Stopping existing FastAPI process (if running)..."
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Stopped any running FastAPI instances."
