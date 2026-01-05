"""
Rotas para validação de documentos
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
from ..controllers.validation_controller import ValidationController

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["validation"])


class ValidationRequest(BaseModel):
    """Request body para validação"""
    texto_documento: str
    modelo_id: Optional[str] = "default"
    use_ai: Optional[bool] = True


@router.post("/validar")
async def validar(request: ValidationRequest):
    """
    Valida documento contra modelo oficial
    Retorna resultado completo da validação
    """
    try:
        resultado = ValidationController.validate_documento(
            texto_documento=request.texto_documento,
            modelo_id=request.modelo_id,
            use_ai=request.use_ai
        )
        return JSONResponse(content=resultado)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro no endpoint validar: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validar/relatorio")
async def gerar_relatorio(request: ValidationRequest):
    """
    Valida documento e gera relatório PDF
    """
    try:
        # Valida documento
        resultado = ValidationController.validate_documento(
            texto_documento=request.texto_documento,
            modelo_id=request.modelo_id,
            use_ai=request.use_ai
        )
        
        # Gera relatório
        report_path = ValidationController.generate_report(resultado)
        
        return FileResponse(
            path=str(report_path),
            filename=report_path.name,
            media_type="application/pdf"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}")
        raise HTTPException(status_code=500, detail=str(e))







