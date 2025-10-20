@echo off
echo == RUN CHECK ==
echo Checking .NET Framework presence...
where /q dotnet
if %ERRORLEVEL%==0 ( echo dotnet found ) else ( echo dotnet not found - ensure .NET installed )
echo Checking MSBuild...
where /q msbuild
if %ERRORLEVEL%==0 ( echo msbuild found ) else ( echo msbuild not found - install Build Tools )
echo Check Inno Setup (ISCC)...
where /q iscc
if %ERRORLEVEL%==0 ( echo Inno Setup compiler found ) else ( echo Inno Setup not found - optional for installer )
pause
