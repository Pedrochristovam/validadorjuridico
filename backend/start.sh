#!/bin/bash
# Script de inicialização para produção (Render)

# Cria diretórios necessários
mkdir -p uploads
mkdir -p reports
mkdir -p modelos

# Executa o servidor
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1

