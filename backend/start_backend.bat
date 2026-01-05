@echo off
echo ========================================
echo Iniciando Backend - Validador Juridico
echo ========================================
echo.

cd /d %~dp0

echo Verificando Python...
py --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.9+ e tente novamente.
    pause
    exit /b 1
)

echo.
echo Verificando dependencias...
py -m pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    py -m pip install -r requirements.txt
)

echo.
echo Iniciando servidor na porta 8000...
echo Backend estara disponivel em: http://localhost:8000
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

py main.py

pause






