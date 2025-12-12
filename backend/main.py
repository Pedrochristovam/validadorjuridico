"""
API FastAPI para Validação Automática de Documentos Jurídicos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa rotas
from src.routes import upload_routes, validation_routes

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cria app FastAPI
app = FastAPI(
    title="Validador Jurídico API",
    description="API para validação automática de documentos jurídicos",
    version="1.0.0"
)

# Configura CORS
import os
cors_origins_str = os.getenv("CORS_ORIGINS", "*")
if cors_origins_str == "*":
    cors_origins = ["*"]
else:
    cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra rotas
app.include_router(upload_routes.router)
app.include_router(validation_routes.router)


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Validador Jurídico API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/uploadDocumento",
            "modelo": "/api/uploadModelo",
            "validar": "/api/validar"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )


if __name__ == "__main__":
    import uvicorn
    
    # Cria diretórios necessários
    Path("uploads").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("modelos").mkdir(exist_ok=True)
    
    # Em produção, não usar reload
    is_production = os.getenv("ENVIRONMENT", "development") == "production"
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=not is_production
    )

