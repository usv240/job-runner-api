Write-Host "Starting FastAPI server..."
cd C:\JobRunnerAPI
Start-Process python -ArgumentList "app/main.py" -NoNewWindow
Write-Host "FastAPI server started successfully."
