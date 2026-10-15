@echo off
echo ======================================================================
echo TESTE COMPLETO DA AUTOMACAO
echo ======================================================================
echo.

echo [1/5] Testando gerador de dashboards...
python gerar_dashboard_conteudo.py
if %ERRORLEVEL% EQU 0 (
    echo ✅ Gerador de dashboards: SUCESSO
) else (
    echo ❌ Gerador de dashboards: FALHA
)
echo.

echo [2/5] Testando classificador de pilares...
python classificar_pilares.py
if %ERRORLEVEL% EQU 0 (
    echo ✅ Classificador: SUCESSO
) else (
    echo ❌ Classificador: FALHA
)
echo.

echo [3/5] Testando pipeline completo...
python pipeline_atualizacao.py
if %ERRORLEVEL% EQU 0 (
    echo ✅ Pipeline: SUCESSO
) else (
    echo ❌ Pipeline: FALHA
)
echo.

echo [4/5] Verificando arquivos gerados...
dir *.html *.csv /o-d
echo.

echo [5/5] Abrindo dashboards...
start dashboard_conteudo.html
start dashboard_recentes.html
echo.

echo ======================================================================
echo TESTE CONCLUIDO
echo ======================================================================
pause