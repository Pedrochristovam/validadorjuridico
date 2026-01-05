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
            if not api_key:
                logger.warning("OPENAI_API_KEY não encontrada; IA desativada para OpenAI")
                return
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as exc:  # noqa: BLE001
                logger.error("Falha ao inicializar cliente OpenAI", exc_info=True)
                self.client = None
        elif self.provider == "groq" and GROQ_AVAILABLE:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                logger.warning("GROQ_API_KEY não encontrada; IA desativada para Groq")
                return
            try:
                self.client = Groq(api_key=api_key)
            except Exception as exc:  # noqa: BLE001
                logger.error("Falha ao inicializar cliente Groq", exc_info=True)
                self.client = None
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
{texto_documento[:12000]}

INSTRUÇÕES DETALHADAS:
1. Analise TODOS os requisitos obrigatórios:

   EXPERIÊNCIA GERAL:
   - Comprovar experiência específica em direito tributário e previdenciário (custeio e/ou benefício)

   LOTE 1 - TRIBUTÁRIO E PREVIDENCIÁRIO:
   - Item (i): 5 defesas administrativas nos últimos 5 anos, valores >= R$ 2.500.000,00, com condução bem-sucedida
   - Item (ii): 5 processos judiciais nos últimos 5 anos, valores >= R$ 2.500.000,00, com condução bem-sucedida
   - Item (iii): Histórico profissional com lista de processos, 5 processos nos últimos 5 anos, valores >= R$ 2.500.000,00, com condução bem-sucedida
   - Item (iv): Capacidade de análise contábil/fiscal/financeira por profissional com formação/especialização contábil

   LOTE 2 - PIS E COFINS (SECURITIZAÇÃO):
   - Item (i): 5 defesas administrativas em securitização de créditos nos últimos 5 anos, valores >= R$ 2.500.000,00, com condução bem-sucedida
   - Item (ii): 5 processos judiciais em securitização de créditos nos últimos 5 anos, valores >= R$ 2.500.000,00, com condução bem-sucedida
   - Item (iii): Histórico profissional em securitização de créditos, 5 processos nos últimos 5 anos, valores >= R$ 2.500.000,00, com condução bem-sucedida
   - Item (iv): Capacidade de análise contábil/fiscal/financeira incluindo securitização de créditos e debêntures

   REGRAS GERAIS:
   - Itens i, ii, iii de ambos os lotes são CUMULATIVOS
   - Comprovação requer: sentenças favoráveis + certidões de trânsito em julgado
   - Item iv pode ser comprovado por: CPA, pós-graduação, MBA ou cursos contábeis/fiscais/financeiros

2. Para cada requisito, verifique EXATAMENTE:
   - Quantidade mínima: 5 (defesas/processos)
   - Valores mínimos: >= R$ 2.500.000,00 (dois milhões e quinhentos mil reais)
   - Período: últimos 5 anos
   - Resultado: condução bem-sucedida / resultado exitoso
   - Área específica: securitização de créditos (para Lote 2)

3. Retorne APENAS um JSON válido com esta estrutura exata:
{{
  "atende": ["experiencia_geral", "lote_1_i", "lote_1_ii", "lote_1_iii", "lote_1_iv", "lote_2_i", "lote_2_ii", "lote_2_iii", "lote_2_iv"],
  "faltando": ["lista", "de", "requisitos", "não", "comprovados"],
  "duvidoso": ["lista", "de", "requisitos", "parcialmente", "comprovados"],
  "evidencias": {{
    "requisito_1": "trecho exato do documento que comprova",
    "requisito_2": "outro trecho relevante"
  }},
  "status_geral": "APROVADO" ou "REPROVADO",
  "motivo": "explicação detalhada do status geral baseado nos requisitos cumulativos"
}}

IMPORTANTE: 
- Retorne APENAS o JSON, sem texto adicional antes ou depois.
- Seja rigoroso: um requisito só está "atende" se TODOS os critérios (quantidade, valor, período, resultado) forem mencionados.
- Lembre-se: itens i, ii, iii são CUMULATIVOS - todos devem estar presentes.
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


