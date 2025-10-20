@echo off
echo Running Listener.exe from bin\Release
if exist "bin\Release\Listener.exe" (
  start "" "bin\Release\Listener.exe"
) else (
  echo bin\Release\Listener.exe not found. Build first.
)
pause
