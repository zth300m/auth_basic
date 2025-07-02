@echo off

echo Checking Python and pip...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not found. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip is not found. Please install pip.
    pause
    exit /b 1
)

echo Installing/Updating Python dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies. Please check the error above.
    pause
    exit /b 1
)
echo =========================================================
echo Uvicorn Up localhost
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause

