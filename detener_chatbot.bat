@echo off
taskkill /FI "WINDOWTITLE eq Django Server" /T /F
taskkill /FI "WINDOWTITLE eq Ngrok" /T /F
