@echo off
chcp 65001 >nul
echo ========================================================
echo   Corrigindo erro do ChromeDriver e instalando dependencias
echo ========================================================
echo.
echo Instalando webdriver-manager (resolve o conflito de versao)...
python -m pip install --upgrade pip
python -m pip install webdriver-manager selenium beautifulsoup4
echo.
echo ✅ Correcao aplicada com sucesso!
echo Agora pode executar o 'rodar_buffer.bat' normalmente.
pause