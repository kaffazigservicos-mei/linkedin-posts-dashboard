@echo off
chcp 65001 >nul
title Buffer Export - LinkedInposts
cd /d "C:\Users\dilma\Documents\Linkedinposts"

echo ========================================================
echo   Exportador de Posts do Buffer
echo   Pasta: C:\Users\dilma\Documents\Linkedinposts
echo ========================================================
echo.

REM Detecta Python automaticamente
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY=python"
) else (
    set "PY=C:\Users\dilma\AppData\Local\Programs\Python\Python314\python.exe"
)

REM Verifica se o script existe
if not exist "buffer_export1.py" (
    echo.
    echo ERRO: buffer_export1.py nao encontrado!
    echo Pasta atual: %cd%
    echo.
    dir /b *.py 2>nul
    pause
    exit /b 1
)

echo Iniciando...
echo.
"%PY%" buffer_export1.py

echo.
echo ========================================================
if %errorlevel% neq 0 (
    echo ERRO: O script finalizou com codigo de erro %errorlevel%
) else (
    echo Script finalizado com sucesso.
)
echo ========================================================
pause