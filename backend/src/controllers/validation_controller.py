"""
Controller para validação de documentos
"""
from fastapi import HTTPException
import logging
from ..services.validation_service import ValidationService
from ..services.report_service import ReportService
from ..utils.file_handler import load_modelo_json
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class ValidationController:
    """Controller para gerenciar validações"""
    
    @staticmethod
    def validate_documento(texto_documento: str, modelo_id: str = "default", use_ai: bool = True) -> dict:
        """
        Valida documento contra modelo oficial
        Se modelo_id for especificado, compara com o texto do modelo
        """
        try:
            import json
            
            # Carrega modelo
            if modelo_id != "default":
                # Tenta carregar modelo específico
                modelo_path = Path("modelos") / f"{modelo_id}.json"
                if not modelo_path.exists():
                    # Se não encontrar, usa o padrão
                    modelo_path = Path("modelo.json")
            else:
                modelo_path = Path("modelo.json")
            
            if not modelo_path.exists():
                raise FileNotFoundError(f"Modelo não encontrado: {modelo_path}")
            
            with open(modelo_path, "r", encoding="utf-8") as f:
                modelo = json.load(f)
            
            # Se o modelo tem texto extraído, usa para comparação
            texto_modelo = modelo.get("texto_extraido", "")
            
            # Se tem texto do modelo, combina com o texto do documento para validação
            # Isso permite comparar o documento com o modelo
            if texto_modelo:
                # Combina texto do modelo e documento para validação mais precisa
                texto_completo = f"MODELO DE REFERÊNCIA:\n{texto_modelo}\n\nDOCUMENTO A VALIDAR:\n{texto_documento}"
            else:
                # Se não tem texto do modelo, usa apenas o documento
                texto_completo = texto_documento
            
            # Determina provider de IA
            ai_provider = os.getenv("AI_PROVIDER", "openai").lower()
            
            # Cria serviço de validação
            validation_service = ValidationService(
                modelo=modelo,
                use_ai=use_ai,
                ai_provider=ai_provider
            )
            
            # Executa validação usando o texto completo (modelo + documento)
            resultado = validation_service.validate(texto_completo)
            
            # Adiciona informações do modelo usado
            resultado["modelo_usado"] = modelo.get("nome", "Padrão")
            resultado["modelo_id"] = modelo_id
            
            return resultado
            
        except FileNotFoundError as e:
            logger.error(f"Modelo não encontrado: {e}")
            raise HTTPException(
                status_code=404,
                detail=f"Modelo {modelo_id} não encontrado"
            )
        except Exception as e:
            logger.error(f"Erro na validação: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao validar documento: {str(e)}"
            )
    
    @staticmethod
    def generate_report(resultado: dict, output_filename: str = None) -> Path:
        """
        Gera relatório PDF da validação
        """
        try:
            if not output_filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"relatorio_validacao_{timestamp}.pdf"
            
            # Garante diretório de relatórios
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            output_path = reports_dir / output_filename
            
            # Gera relatório
            report_service = ReportService()
            report_path = report_service.generate_report(resultado, output_path)
            
            return report_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao gerar relatório: {str(e)}"
            )


