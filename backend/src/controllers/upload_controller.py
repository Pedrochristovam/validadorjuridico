"""
Controller para upload de arquivos
"""
from fastapi import UploadFile, HTTPException
from pathlib import Path
import logging
from ..services.extraction_service import extract_text
from ..utils.file_handler import save_uploaded_file, save_modelo_json

logger = logging.getLogger(__name__)


class UploadController:
    """Controller para gerenciar uploads"""
    
    @staticmethod
    async def upload_documento(file: UploadFile) -> dict:
        """
        Faz upload e extrai texto de documento (PDF/DOCX)
        """
        try:
            # Valida extensão
            filename = file.filename
            if not filename:
                raise HTTPException(status_code=400, detail="Nome de arquivo não fornecido")
            
            ext = Path(filename).suffix.lower()
            if ext not in [".pdf", ".docx", ".doc"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Formato não suportado: {ext}. Use PDF ou DOCX."
                )
            
            # Lê arquivo
            file_content = await file.read()
            
            # Salva arquivo temporariamente
            file_path = save_uploaded_file(file_content, filename)
            
            # Extrai texto
            texto_extraido = extract_text(file_path, filename)
            
            if not texto_extraido or len(texto_extraido.strip()) < 10:
                raise HTTPException(
                    status_code=400,
                    detail="Não foi possível extrair texto do documento. Verifique se o arquivo está válido."
                )
            
            return {
                "success": True,
                "message": "Documento processado com sucesso",
                "texto_extraido": texto_extraido,
                "filename": filename
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro ao processar upload: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar documento: {str(e)}"
            )
    
    @staticmethod
    async def upload_modelo(nome: str, file: UploadFile = None, modelo_data: dict = None) -> dict:
        """
        Faz upload e salva modelo oficial
        Aceita arquivo Word (.docx) ou JSON com estrutura do modelo
        """
        try:
            import json
            import os
            from datetime import datetime
            
            # Cria diretório de modelos se não existir
            modelos_dir = Path("modelos")
            modelos_dir.mkdir(exist_ok=True)
            
            modelo_id = f"modelo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            modelo_info = {
                "id": modelo_id,
                "nome": nome,
                "created_at": datetime.now().isoformat(),
            }
            
            # Se foi enviado um arquivo Word
            if file and file.filename:
                ext = Path(file.filename).suffix.lower()
                if ext not in [".docx", ".doc", ".pdf"]:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Formato não suportado: {ext}. Use DOCX, DOC ou PDF."
                    )
                
                # Lê e salva arquivo
                file_content = await file.read()
                file_path = save_uploaded_file(file_content, file.filename)
                
                # Extrai texto do arquivo
                texto_modelo = extract_text(file_path, file.filename)
                
                if not texto_modelo or len(texto_modelo.strip()) < 10:
                    raise HTTPException(
                        status_code=400,
                        detail="Não foi possível extrair texto do arquivo modelo. Verifique se o arquivo está válido."
                    )
                
                modelo_info["arquivo_original"] = file.filename
                modelo_info["texto_extraido"] = texto_modelo
                modelo_info["tipo"] = "arquivo"
                
            # Se foi enviado JSON com estrutura
            elif modelo_data:
                if "modelo" not in modelo_data or "requisitos" not in modelo_data:
                    raise HTTPException(
                        status_code=400,
                        detail="Estrutura do modelo inválida. Deve conter 'modelo' e 'requisitos'"
                    )
                modelo_info.update(modelo_data)
                modelo_info["tipo"] = "json"
            
            else:
                raise HTTPException(
                    status_code=400,
                    detail="É necessário enviar um arquivo Word ou JSON com a estrutura do modelo"
                )
            
            # Salva modelo em JSON
            modelo_filename = f"{modelo_id}.json"
            modelo_path = modelos_dir / modelo_filename
            
            with open(modelo_path, "w", encoding="utf-8") as f:
                json.dump(modelo_info, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "message": "Modelo salvo com sucesso",
                "modelo_id": modelo_id,
                "modelo_path": str(modelo_path),
                "nome": nome
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro ao salvar modelo: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao salvar modelo: {str(e)}"
            )


