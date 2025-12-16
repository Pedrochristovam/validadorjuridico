@echo off
echo ========================================
echo Iniciando Sistema Validador Juridico
echo ========================================
echo.

cd /d %~dp0

echo Iniciando Backend...
start "Backend - Validador Juridico" cmd /k "cd backend && py main.py"

echo Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

echo.
echo Iniciando Frontend...
start "Frontend - Validador Juridico" cmd /k "npm run dev"

echo.
echo ========================================
echo Sistema iniciado!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Feche esta janela para manter os servidores rodando.
echo Para parar, feche as janelas do Backend e Frontend.
echo.
pause

