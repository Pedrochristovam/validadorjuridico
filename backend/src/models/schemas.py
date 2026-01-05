"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel
from typing import List, Dict, Optional


class ValidationResult(BaseModel):
    """Schema do resultado de validação"""
    corretos: List[str] = []
    faltando: List[str] = []
    duvidosos: List[str] = []
    evidencias: Dict[str, str] = {}
    status_geral: str = "REPROVADO"


class UploadResponse(BaseModel):
    """Resposta do upload de documento"""
    success: bool
    message: str
    texto_extraido: Optional[str] = None
    filename: Optional[str] = None


class ValidationRequest(BaseModel):
    """Request para validação"""
    texto_documento: str
    modelo_id: Optional[str] = "default"







