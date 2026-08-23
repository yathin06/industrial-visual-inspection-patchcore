@echo off
cd /d C:\Quality
title AI Visual Inspection System

echo =====================================================
echo AI VISUAL INSPECTION SYSTEM
echo =====================================================
echo.

echo Starting Docker containers...
docker compose up -d

echo.
echo Waiting for FastAPI and PatchCore model...
powershell -Command "for ($i=0; $i -lt 60; $i++) { try { $r = Invoke-RestMethod -Uri http://127.0.0.1:8000/health -TimeoutSec 3; if ($r.model_loaded -eq $true) { Write-Host 'API ready. PatchCore model loaded.'; exit 0 } } catch {} Start-Sleep -Seconds 2 }; Write-Host 'API not ready in time.'; exit 1"

echo.
echo Opening dashboard...
start http://localhost:8501

echo.
echo Resetting counters...
powershell -Command "Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/reset"

goto MENU


:MENU
cls
echo =====================================================
echo AI VISUAL INSPECTION SYSTEM
echo =====================================================
echo Dashboard: http://localhost:8501
echo.
echo Select inspection option:
echo.
echo 0  - Send GOOD image
echo 1  - Send DEFECTIVE image
echo 2  - Send 15 mixed samples
echo 8  - Reset counters
echo 9  - Stop Docker system
echo.
echo =====================================================
choice /c 01289 /n /m "Press 0, 1, 2, 8, or 9: "

if errorlevel 5 goto STOP_SYSTEM
if errorlevel 4 goto RESET_COUNTERS
if errorlevel 3 goto BATCH_15
if errorlevel 2 goto DEFECTIVE_IMAGE
if errorlevel 1 goto GOOD_IMAGE


:GOOD_IMAGE
cls
echo =====================================================
echo SENDING GOOD IMAGE
echo =====================================================
echo.

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\good\000.png" "GOOD SAMPLE"

echo.
echo Expected dashboard result: OK
echo.
timeout /t 3 >nul
goto MENU


:DEFECTIVE_IMAGE
cls
echo =====================================================
echo SENDING DEFECTIVE IMAGE
echo =====================================================
echo.

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\bent\000.png" "DEFECTIVE BENT SAMPLE"

echo.
echo Expected dashboard result: NG
echo.
timeout /t 3 >nul
goto MENU


:BATCH_15
cls
echo =====================================================
echo SENDING 15 MIXED INSPECTION SAMPLES
echo =====================================================
echo.

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\good\000.png" "GOOD 000"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\good\001.png" "GOOD 001"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\good\002.png" "GOOD 002"

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\bent\000.png" "BENT 000"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\bent\001.png" "BENT 001"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\bent\002.png" "BENT 002"

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\color\000.png" "COLOR 000"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\color\001.png" "COLOR 001"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\color\002.png" "COLOR 002"

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\flip\000.png" "FLIP 000"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\flip\001.png" "FLIP 001"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\flip\002.png" "FLIP 002"

call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\scratch\000.png" "SCRATCH 000"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\scratch\001.png" "SCRATCH 001"
call :SEND_IMAGE "C:\Quality\datasets\MVTecAD\metal_nut\test\scratch\002.png" "SCRATCH 002"

echo.
echo 15-sample inspection completed.
echo.
echo Current production status:
powershell -Command "Invoke-RestMethod -Uri http://127.0.0.1:8000/status"
echo.
timeout /t 5 >nul
goto MENU


:RESET_COUNTERS
cls
echo Resetting counters...
powershell -Command "Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/reset"
echo.
echo Counters reset.
timeout /t 2 >nul
goto MENU


:STOP_SYSTEM
cls
echo Stopping Docker containers...
docker compose down
echo.
echo System stopped.
timeout /t 3 >nul
exit


:SEND_IMAGE
echo Sending: %~2
curl.exe -s -X POST "http://127.0.0.1:8000/inspect" -F "file=@%~1"
echo.
timeout /t 1 >nul
exit /b