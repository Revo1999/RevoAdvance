@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\course.ps1" %*
set "lessonExit=%errorlevel%"
if not "%lessonExit%"=="0" pause
exit /b %lessonExit%
