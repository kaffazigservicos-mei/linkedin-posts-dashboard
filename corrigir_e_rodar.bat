@echo off
chcp 65001 >nul
title Corrigindo e Rodando LinkedInposts
cd /d "C:\Users\dilma\Documents\Linkedinposts"

echo ========================================================
echo   Instalando dependencias obrigatorias...
echo ========================================================
echo.

set "PY=C:\Users\dilma\AppData\Local\Programs\Python\Python314\python.exe"

if not exist "%PY%" (
    echo Python nao encontrado no caminho padrao. Tentando 'python' do sistema...
    set "PY=python"
)

echo Instalando selenium e webdriver-manager...
"%PY%" -m pip install --upgrade pip
"%PY%" -m pip install selenium webdriver-manager

echo.
echo ========================================================
echo   Iniciando o script buffer_export1.py...
echo ========================================================
echo.

"%PY%" buffer_export1.py

echo.
pause