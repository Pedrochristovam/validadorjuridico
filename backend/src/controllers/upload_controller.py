"""
Controller para upload de arquivos
"""
from fastapi import UploadFile, HTTPException  # type: ignore
from pathlib import Path
import logging
import os
from ..services.extraction_service import extract_text
from ..utils.file_handler import save_uploaded_file, save_modelo_json

logger = logging.getLogger(__name__)

# Limites de tamanho configuráveis (em bytes)
# Padrão: 50MB para documentos, pode ser configurado via variável de ambiente
MAX_FILE_SIZE_DOCUMENTO = int(os.getenv("MAX_FILE_SIZE_DOCUMENTO", 50 * 1024 * 1024))  # 50MB padrão
MAX_FILE_SIZE_MODELO = int(os.getenv("MAX_FILE_SIZE_MODELO", 20 * 1024 * 1024))  # 20MB padrão


class UploadController:
    """Controller para gerenciar uploads"""
    
    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """Formata tamanho do arquivo em formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
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
            
            # Lê arquivo em chunks para verificar tamanho antes de processar tudo
            file_content = b""
            total_size = 0
            
            while True:
                chunk = await file.read(1024 * 1024)  # Lê em chunks de 1MB
                if not chunk:
                    break
                total_size += len(chunk)
                
                # Verifica limite durante o upload
                if total_size > MAX_FILE_SIZE_DOCUMENTO:
                    max_size_mb = MAX_FILE_SIZE_DOCUMENTO / (1024 * 1024)
                    raise HTTPException(
                        status_code=413,
                        detail=f"Arquivo muito grande. Tamanho máximo permitido: {max_size_mb:.0f}MB. "
                               f"Tamanho do arquivo: {UploadController._format_file_size(total_size)}"
                    )
                file_content += chunk
            
            # Verifica tamanho final
            if len(file_content) > MAX_FILE_SIZE_DOCUMENTO:
                max_size_mb = MAX_FILE_SIZE_DOCUMENTO / (1024 * 1024)
                raise HTTPException(
                    status_code=413,
                    detail=f"Arquivo muito grande. Tamanho máximo permitido: {max_size_mb:.0f}MB. "
                           f"Tamanho do arquivo: {UploadController._format_file_size(len(file_content))}"
                )
            
            # Salva arquivo temporariamente
            file_path = save_uploaded_file(file_content, filename)
            
            # Extrai texto
            texto_extraido = extract_text(file_path, filename)
            
            if not texto_extraido or len(texto_extraido.strip()) < 10:
                raise HTTPException(
                    status_code=400,
                    detail="Não foi possível extrair texto do documento. Verifique se o arquivo está válido."
                )
            
            file_size_mb = len(file_content) / (1024 * 1024)
            logger.info(f"Documento processado: {filename} ({file_size_mb:.2f}MB)")
            
            return {
                "success": True,
                "message": "Documento processado com sucesso",
                "texto_extraido": texto_extraido,
                "filename": filename,
                "file_size": len(file_content),
                "file_size_mb": round(file_size_mb, 2)
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
                
                # Lê arquivo em chunks para verificar tamanho
                file_content = b""
                total_size = 0
                
                while True:
                    chunk = await file.read(1024 * 1024)  # Lê em chunks de 1MB
                    if not chunk:
                        break
                    total_size += len(chunk)
                    
                    # Verifica limite durante o upload
                    if total_size > MAX_FILE_SIZE_MODELO:
                        max_size_mb = MAX_FILE_SIZE_MODELO / (1024 * 1024)
                        raise HTTPException(
                            status_code=413,
                            detail=f"Arquivo modelo muito grande. Tamanho máximo permitido: {max_size_mb:.0f}MB. "
                                   f"Tamanho do arquivo: {UploadController._format_file_size(total_size)}"
                        )
                    file_content += chunk
                
                # Verifica tamanho final
                if len(file_content) > MAX_FILE_SIZE_MODELO:
                    max_size_mb = MAX_FILE_SIZE_MODELO / (1024 * 1024)
                    raise HTTPException(
                        status_code=413,
                        detail=f"Arquivo modelo muito grande. Tamanho máximo permitido: {max_size_mb:.0f}MB. "
                               f"Tamanho do arquivo: {UploadController._format_file_size(len(file_content))}"
                    )
                
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


