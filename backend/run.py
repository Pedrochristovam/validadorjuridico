#!/usr/bin/env python3
"""
Script de inicialização do servidor
"""
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Cria diretórios necessários
Path("uploads").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

