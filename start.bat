@echo off
echo Starting FastAPI server...
start cmd /k "uvicorn api:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak

echo Starting ngrok tunnel...
start cmd /k "ngrok http 8000"

echo Both are running. Check the ngrok window for your public link.
