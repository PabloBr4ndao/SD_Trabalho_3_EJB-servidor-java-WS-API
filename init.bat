@echo off
title PAINEL DE CONTROLE - SISTEMAS DISTRIBUIDOS

:: ==========================================
:: 1. PREPARACAO E SERVIDOR JAVA
:: ==========================================
cls
echo ==========================================
echo [1/2] PREPARANDO SERVIDOR JAVA...
echo        (Compilacao + Execucao)
echo ==========================================

cd servidor-api
call mvn clean package
echo .....................................................................
echo ....          Iniciando Servidor na porta 8080...                ....
echo .....................................................................
start "SERVIDOR JAVA" /min cmd /k "java -cp target/servidor-api-1.0-SNAPSHOT.jar;target/lib/* com.sd.server.ApiServer"
cd ..

timeout /t 5 /nobreak >nul

:: ==========================================
:: 2. INTERFACES WEB (STREAMLIT)
:: ==========================================
echo.
echo [2/2] SUBINDO INTERFACES WEB (Background)...

start "DASHBOARD ADMIN" /min cmd /k "streamlit run python_files/admin.py --server.port=8502"

timeout /t 2 /nobreak >nul

start "CLIENTE WEB" /min cmd /k "streamlit run python_files/site_restaurante.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true"

:: ==========================================
:: 3. MENU DE CONTROLE (LOOP)
:: ==========================================

:MENU
cls
echo =================================================================
echo                        SISTEMA RODANDO...
echo =================================================================
echo.
echo   ..............................................................
echo    SEU ENDERECO IP NA REDE:
ipconfig | findstr "IPv4"
echo   ..............................................................
echo.
:: Note o uso do ^ antes do | abaixo
echo   ^| TUDO PRONTO! Acesse...
echo   ^|  - Cliente :             http://[SEU_IP]:8501   ---- (Usando outro dispositivo na mesma rede)
echo   ^|  - Admin (PC - Local) :  http://localhost:8502
echo.
echo.
echo ===============================================
echo ^|            COMANDOS RAPIDOS:                ^|
echo ===============================================
echo   [p] + Enter --- Rodar Cliente Python (Script)
echo   [j] + Enter --- Rodar Cliente Node.js
echo   [Enter] ------- FECHAR TUDO E SAIR
echo ===============================================
echo.

set "opcao="
set /p "opcao=Digite sua opcao: "

:: Se apertar apenas ENTER (variavel vazia), vai para o fim
if "%opcao%"=="" goto FIM

:: Se digitar P ou p
if /i "%opcao%"=="p" (
    echo.
    echo Executando Cliente Python...
    start "CLIENTE PYTHON" cmd /k "python python_files\cliente.py"
    timeout /t 1 >nul
    goto MENU
)

:: Se digitar J ou j
if /i "%opcao%"=="j" (
    echo.
    echo Executando Cliente Node.js...
    start "CLIENTE NODE" cmd /k "node cliente-node/cliente.js"
    timeout /t 1 >nul
    goto MENU
)

:: Se digitar outra coisa volta ao inicio
goto MENU

:FIM
echo.
echo Encerrando lancador... (As janelas abertas continuarao rodando)
timeout /t 2 >nul
exit