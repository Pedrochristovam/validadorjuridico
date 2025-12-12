"""
Serviço de validação com IA (OpenAI/Groq/Claude)
"""
import os
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Tenta importar diferentes clientes de IA
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class AIValidator:
    """Validador usando IA para análise inteligente"""
    
    def __init__(self, provider: str = "openai"):
        """
        Inicializa o validador de IA
        provider: "openai", "groq" ou "claude"
        """
        self.provider = provider.lower()
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa o cliente de IA baseado no provider"""
        if self.provider == "openai" and OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                logger.warning("OPENAI_API_KEY não encontrada")
        elif self.provider == "groq" and GROQ_AVAILABLE:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self.client = Groq(api_key=api_key)
            else:
                logger.warning("GROQ_API_KEY não encontrada")
        else:
            logger.warning(f"Provider {self.provider} não disponível ou não configurado")
    
    def validate(self, texto_documento: str, modelo: Dict) -> Dict:
        """
        Valida documento usando IA
        Retorna resultado estruturado
        """
        if not self.client:
            logger.warning("Cliente de IA não disponível, retornando resultado vazio")
            return {
                "atende": [],
                "faltando": [],
                "duvidoso": [],
                "evidencias": {},
                "status_geral": "REPROVADO"
            }
        
        prompt = self._build_prompt(texto_documento, modelo)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Erro ao validar com IA: {e}")
            return {
                "atende": [],
                "faltando": [],
                "duvidoso": [],
                "evidencias": {"erro": str(e)},
                "status_geral": "ERRO"
            }
    
    def _build_prompt(self, texto_documento: str, modelo: Dict) -> str:
        """Constrói o prompt para a IA"""
        requisitos = modelo.get("requisitos", {})
        
        prompt = f"""Você é um especialista em análise de documentos jurídicos. Compare o documento enviado com o modelo oficial abaixo e analise TODOS os requisitos obrigatórios.

MODELO OFICIAL:
{json.dumps(modelo, ensure_ascii=False, indent=2)}

DOCUMENTO ENVIADO:
{texto_documento[:8000]}  # Limita tamanho

INSTRUÇÕES:
1. Analise todos os requisitos dos Lotes 1 e 2, incluindo:
   - Experiência geral em direito tributário e previdenciário
   - Lote 1: Itens i, ii, iii, iv (Tributário e Previdenciário)
   - Lote 2: Itens i, ii, iii, iv (PIS e COFINS/Securitização)
   - Regras de cumulatividade (itens i, ii, iii são cumulativos)
   - Comprovações obrigatórias (sentenças favoráveis, certidões, capacidade contábil)

2. Para cada requisito, verifique:
   - Quantidade mínima (ex: 5 defesas, 5 processos)
   - Valores mínimos (ex: >= 2.500.000)
   - Período (últimos 5 anos)
   - Comprovações específicas

3. Retorne APENAS um JSON válido com esta estrutura exata:
{{
  "atende": ["lista", "de", "requisitos", "completamente", "atendidos"],
  "faltando": ["lista", "de", "requisitos", "não", "comprovados"],
  "duvidoso": ["lista", "de", "requisitos", "parcialmente", "comprovados"],
  "evidencias": {{
    "requisito_1": "trecho do documento que justifica",
    "requisito_2": "outro trecho relevante"
  }},
  "status_geral": "APROVADO" ou "REPROVADO",
  "motivo": "explicação breve do status geral"
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional antes ou depois.
"""
        return prompt
    
    def _call_ai(self, prompt: str) -> str:
        """Chama a API de IA"""
        if self.provider == "openai" and self.client:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # ou gpt-4, gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de documentos jurídicos. Sempre retorne apenas JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        
        elif self.provider == "groq" and self.client:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",  # ou outro modelo Groq
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de documentos jurídicos. Sempre retorne apenas JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        
        else:
            raise Exception(f"Provider {self.provider} não configurado corretamente")
    
    def _parse_response(self, response: str) -> Dict:
        """Parseia a resposta da IA para JSON"""
        try:
            # Remove markdown code blocks se existirem
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()
            
            return json.loads(response_clean)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear resposta da IA: {e}")
            logger.error(f"Resposta recebida: {response[:500]}")
            return {
                "atende": [],
                "faltando": [],
                "duvidoso": [],
                "evidencias": {"erro": "Erro ao parsear resposta da IA"},
                "status_geral": "ERRO"
            }


