"""
Rotas para upload de arquivos
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Dict, Optional
import logging
from ..controllers.upload_controller import UploadController

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/uploadDocumento")
async def upload_documento(file: UploadFile = File(...)):
    """
    Upload de documento (PDF ou DOCX) e extração de texto
    """
    try:
        resultado = await UploadController.upload_documento(file)
        return JSONResponse(content=resultado)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro no endpoint uploadDocumento: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/uploadModelo")
async def upload_modelo(
    nome: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    Upload e salvamento do modelo oficial
    Aceita arquivo Word (.docx) como modelo
    """
    try:
        resultado = await UploadController.upload_modelo(
            nome=nome,
            file=file,
            modelo_data=None
        )
        return JSONResponse(content=resultado)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro no endpoint uploadModelo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modelos")
async def listar_modelos():
    """
    Lista todos os modelos salvos
    """
    try:
        from ..utils.file_handler import list_modelos
        modelos = list_modelos()
        return JSONResponse(content={"modelos": modelos})
    except Exception as e:
        logger.error(f"Erro ao listar modelos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/modelos/{modelo_id}")
async def deletar_modelo(modelo_id: str):
    """
    Deleta um modelo específico
    """
    try:
        from ..utils.file_handler import delete_modelo
        resultado = delete_modelo(modelo_id)
        return JSONResponse(content=resultado)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao deletar modelo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


