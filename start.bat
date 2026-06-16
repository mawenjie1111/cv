@echo off
REM Start the FastAPI backend and Vue frontend in separate windows.
setlocal
set "ROOT_DIR=%~dp0"

echo ==> Installing backend dependencies
python -m pip install -r "%ROOT_DIR%backend\requirements.txt"

echo ==> Installing frontend dependencies
pushd "%ROOT_DIR%frontend"
call npm install
popd

echo ==> Starting backend at http://localhost:8000
start "backend" cmd /k "cd /d "%ROOT_DIR%backend" && python -m uvicorn app.main:app --reload"

echo ==> Starting frontend at http://localhost:5173
start "frontend" cmd /k "cd /d "%ROOT_DIR%frontend" && npm run dev"

echo ==> Both started in separate windows. Close those windows to stop.
endlocal
