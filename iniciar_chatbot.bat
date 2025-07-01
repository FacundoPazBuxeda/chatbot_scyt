@echo off
cd /d C:\scyt-assistant

:: Activar entorno virtual
call venv\Scripts\activate.bat

:: Iniciar Django en segundo plano
start "Django Server" cmd /k "python manage.py runserver"

:: Esperar un poco para que Django arranque antes de ngrok
timeout /t 10 > nul

:: Iniciar ngrok (puerto 8000, ajustá si usás otro)
start "Ngrok" cmd /k "C:\ngrok\ngrok.exe http --url=feasible-light-krill.ngrok-free.app 8000"

