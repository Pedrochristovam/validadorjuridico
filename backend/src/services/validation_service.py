"""
Serviço principal de validação que combina regras e IA
"""
from typing import Dict
import logging
from .rule_validator import RuleValidator
from .ai_validator import AIValidator

logger = logging.getLogger(__name__)


class ValidationService:
    """Serviço que combina validação programada e IA"""
    
    def __init__(self, modelo: Dict, use_ai: bool = True, ai_provider: str = "openai"):
        self.modelo = modelo
        self.rule_validator = RuleValidator(modelo)
        self.use_ai = use_ai
        self.ai_validator = AIValidator(provider=ai_provider) if use_ai else None
    
    def validate(self, texto_documento: str) -> Dict:
        """
        Valida documento combinando regras programadas e IA
        Retorna resultado final consolidado
        """
        # Validação com regras programadas
        resultado_regras = self.rule_validator.validate(texto_documento)
        
        # Validação com IA (se habilitada)
        resultado_ai = {}
        if self.use_ai and self.ai_validator:
            try:
                resultado_ai = self.ai_validator.validate(texto_documento, self.modelo)
            except Exception as e:
                logger.error(f"Erro na validação IA: {e}")
                resultado_ai = {}
        
        # Consolida resultados
        resultado_final = self._consolidate_results(resultado_regras, resultado_ai)
        
        return resultado_final
    
    def _consolidate_results(self, regras: Dict, ai: Dict) -> Dict:
        """
        Consolida resultados de regras programadas e IA
        Prioriza regras programadas, mas incorpora insights da IA
        """
        resultado = {
            "corretos": [],
            "faltando": [],
            "duvidosos": [],
            "evidencias": {},
            "status_geral": "REPROVADO"
        }
        
        # Adiciona resultados das regras programadas
        resultado["corretos"].extend(regras.get("corretos", []))
        resultado["faltando"].extend(regras.get("faltando", []))
        resultado["duvidosos"].extend(regras.get("duvidosos", []))
        resultado["evidencias"].update(regras.get("evidencias", {}))
        
        # Incorpora insights da IA (se disponível)
        if ai:
            # Adiciona requisitos que a IA identificou como atendidos
            ai_atende = ai.get("atende", [])
            for item in ai_atende:
                if item not in resultado["corretos"] and item not in resultado["duvidosos"]:
                    resultado["corretos"].append(item)
            
            # Adiciona requisitos faltando identificados pela IA
            ai_faltando = ai.get("faltando", [])
            for item in ai_faltando:
                if item not in resultado["faltando"]:
                    resultado["faltando"].append(item)
            
            # Adiciona evidências da IA
            ai_evidencias = ai.get("evidencias", {})
            resultado["evidencias"].update(ai_evidencias)
            
            # Usa status da IA se mais restritivo
            ai_status = ai.get("status_geral", "REPROVADO")
            if ai_status == "REPROVADO" and resultado["status_geral"] == "APROVADO":
                resultado["status_geral"] = "REPROVADO"
            elif ai_status == "APROVADO" and len(resultado["faltando"]) == 0:
                resultado["status_geral"] = "APROVADO"
        
        # Determina status geral final baseado nos requisitos obrigatórios
        requisitos_obrigatorios = [
            "experiencia_geral",
            "lote_1_i", "lote_1_ii", "lote_1_iii", "lote_1_iv",
            "lote_2_i", "lote_2_ii", "lote_2_iii", "lote_2_iv",
            "comprovacoes"
        ]
        
        faltando_obrigatorios = [req for req in requisitos_obrigatorios if req in resultado["faltando"]]
        corretos_obrigatorios = [req for req in requisitos_obrigatorios if req in resultado["corretos"]]
        
        # Se não há requisitos obrigatórios faltando e há requisitos corretos, aprova
        if len(faltando_obrigatorios) == 0 and len(corretos_obrigatorios) >= len(requisitos_obrigatorios) * 0.7:
            resultado["status_geral"] = "APROVADO"
        # Se a IA retornou APROVADO e não há muitos faltando, considera aprovar
        elif ai and ai.get("status_geral") == "APROVADO" and len(faltando_obrigatorios) <= 2:
            resultado["status_geral"] = "APROVADO"
        else:
            resultado["status_geral"] = "REPROVADO"
        
        return resultado

