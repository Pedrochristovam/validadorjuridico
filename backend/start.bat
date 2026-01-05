@echo off
REM Script de inicialização para produção (Windows/Render)

REM Cria diretórios necessários
if not exist uploads mkdir uploads
if not exist reports mkdir reports
if not exist modelos mkdir modelos

REM Executa o servidor
uvicorn main:app --host 0.0.0.0 --port %PORT% --workers 1






