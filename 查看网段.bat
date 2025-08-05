@echo off
for /L %%i in (1,1,254) do (
    ping -n 1 -w 100 192.168.0.%%i >nul
    if not errorlevel 1 echo 192.168.0.%%i is active
)
pause
