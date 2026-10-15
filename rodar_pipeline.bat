@echo off
chcp 65001 >nul
title Pipeline Semanal - LinkedInposts
cd /d "C:\Users\dilma\Documents\Linkedinposts"

set "PY=C:\Users\dilma\AppData\Local\Programs\Python\Python314\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo   Pipeline Semanal de Atualizacao
echo   Data/Hora: %date% %time%
echo ============================================================
echo.

"%PY%" pipeline_atualizacao.py

echo.
echo ============================================================
echo   Pipeline finalizado.
echo ============================================================
pause