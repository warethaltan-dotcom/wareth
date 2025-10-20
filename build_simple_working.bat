@echo off
title 🏗️ Build SIMPLE WORKING Listener
color 0a

echo ===============================================
echo      SIMPLE WORKING LISTENER
echo ===============================================
echo.

echo 🗑️  Cleaning old processes...
taskkill /F /IM listener_simple_working.exe 2>nul
taskkill /F /IM listener_debug_callerid.exe 2>nul
del C:\listener.lock 2>nul

echo 🏗️  Building Simple Working version...
pyinstaller --onefile --noconsole listener_simple_working.py

if exist "dist\listener_simple_working.exe" (
    copy "dist\listener_simple_working.exe" "listener_simple_working.exe" /Y
    echo ✅ SIMPLE WORKING VERSION BUILT!
    echo.
    echo 📋 GUARANTEED FEATURES:
    echo ✅ Updates CaCallstatus on ANY Dial event
    echo ✅ Clears CaCallstatus on ANY Hangup event  
    echo ✅ Simple caller ID extraction
    echo ✅ Logs to C:\listener_simple.log
    echo.
    echo 🚀 TEST INSTRUCTIONS:
    echo 1. Run listener_simple_working.exe
    echo 2. Check C:\listener_simple.log - should see "STARTING"
    echo 3. Make test call to your extension
    echo 4. Check log - should see "CALL DETECTED" and "CAPTURED CALLER"
    echo 5. Check C:\OMEGASYS\CaCallstatus.dat - should have caller ID
    echo 6. Hang up call - should see "CALL ENDED" and file cleared
    echo.
) else (
    echo ❌ Build failed!
)

pause