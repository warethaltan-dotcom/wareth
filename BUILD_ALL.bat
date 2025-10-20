@echo off
setlocal
echo Building Listener solution (Release)...
if not exist Listener.sln (
  echo Listener.sln not found. Make sure you are in project root.
  pause
  exit /b 1
)
msbuild Listener.sln /t:Build /p:Configuration=Release
if %ERRORLEVEL% neq 0 (
  echo Build failed.
  pause
  exit /b 1
)
echo Build succeeded.
echo Now creating installer (if Inno Setup is installed)...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
  "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" Installer\ListenerSetup.iss
  if %ERRORLEVEL%==0 echo Installer created.
) else (
  echo Inno Setup compiler not found at default path. If installed elsewhere, update BUILD_ALL.bat.
)
pause
