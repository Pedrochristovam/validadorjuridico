"""
Validador com regras programadas fixas
"""
import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RuleValidator:
    """Validação baseada em regras programadas"""
    
    def __init__(self, modelo: Dict):
        self.modelo = modelo
        self.requisitos = modelo.get("requisitos", {})
    
    def validate(self, texto: str) -> Dict:
        """
        Valida o documento usando regras programadas
        Retorna dict com corretos, faltando, duvidosos
        """
        texto_lower = texto.lower()
        resultado = {
            "corretos": [],
            "faltando": [],
            "duvidosos": [],
            "evidencias": {}
        }
        
        # Validação de experiência geral
        self._validate_experiencia_geral(texto_lower, resultado)
        
        # Validação Lote 1
        self._validate_lote_1(texto_lower, resultado)
        
        # Validação Lote 2
        self._validate_lote_2(texto_lower, resultado)
        
        # Validação de comprovações obrigatórias
        self._validate_comprovacoes(texto_lower, resultado)
        
        return resultado
    
    def _validate_experiencia_geral(self, texto: str, resultado: Dict):
        """Valida experiência geral em direito tributário e previdenciário"""
        requisito = self.requisitos.get("experiencia_geral", "")
        
        termos_tributario = ["tributário", "tributaria", "fiscal", "imposto"]
        termos_previdenciario = ["previdenciário", "previdenciaria", "inss", "benefício", "custeio"]
        
        tem_tributario = any(termo in texto for termo in termos_tributario)
        tem_previdenciario = any(termo in texto for termo in termos_previdenciario)
        
        if tem_tributario and tem_previdenciario:
            resultado["corretos"].append("experiencia_geral")
            resultado["evidencias"]["experiencia_geral"] = "Menciona direito tributário e previdenciário"
        else:
            resultado["faltando"].append("experiencia_geral")
            resultado["evidencias"]["experiencia_geral"] = "Não encontrou menção completa a direito tributário e previdenciário"
    
    def _validate_lote_1(self, texto: str, resultado: Dict):
        """Valida requisitos do Lote 1"""
        lote_1 = self.requisitos.get("lote_1", {})
        
        # Item i: 5 defesas administrativas >= 2.500.000
        self._validate_item_i(texto, lote_1.get("i", ""), "lote_1_i", resultado)
        
        # Item ii: 5 processos judiciais >= 2.500.000
        self._validate_item_ii(texto, lote_1.get("ii", ""), "lote_1_ii", resultado)
        
        # Item iii: Histórico profissional
        self._validate_item_iii(texto, lote_1.get("iii", ""), "lote_1_iii", resultado)
        
        # Item iv: Capacidade contábil
        self._validate_item_iv(texto, lote_1.get("iv", ""), "lote_1_iv", resultado)
    
    def _validate_lote_2(self, texto: str, resultado: Dict):
        """Valida requisitos do Lote 2"""
        lote_2 = self.requisitos.get("lote_2", {})
        
        # Item i: 5 defesas administrativas securitização >= 2.500.000
        self._validate_item_i_securitizacao(texto, lote_2.get("i", ""), "lote_2_i", resultado)
        
        # Item ii: 5 processos judiciais securitização >= 2.500.000
        self._validate_item_ii_securitizacao(texto, lote_2.get("ii", ""), "lote_2_ii", resultado)
        
        # Item iii: Histórico profissional securitização
        self._validate_item_iii_securitizacao(texto, lote_2.get("iii", ""), "lote_2_iii", resultado)
        
        # Item iv: Capacidade contábil securitização
        self._validate_item_iv_securitizacao(texto, lote_2.get("iv", ""), "lote_2_iv", resultado)
    
    def _validate_item_i(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item i: 5 defesas administrativas >= 2.500.000 nos últimos 5 anos com resultado exitoso"""
        # Busca por valores >= 2.500.000 (aceita R$ 2.500.000,00, 2.500.000, etc)
        valores = re.findall(r'(?:r\$\s*)?([\d\.]+(?:\.\d{3})*(?:,\d{2})?)', texto, re.IGNORECASE)
        valores_altos = [v for v in valores if self._parse_value(v) >= 2500000]
        
        termos_defesa = ["defesa administrativa", "defesas administrativas", "defesa perante", 
                        "receita federal", "receita estadual", "receita municipal", "previdenciário"]
        tem_defesa = any(termo in texto for termo in termos_defesa)
        
        # Busca por quantidade (5 ou "pelo menos 5")
        tem_quantidade = re.search(r'\b(5|cinco|pelo menos 5|mínimo de 5)\b', texto, re.IGNORECASE)
        
        # Busca por "últimos 5 anos"
        tem_tempo = re.search(r'(últimos?\s*5\s*anos?|5\s*anos?|cinco\s*anos?)', texto, re.IGNORECASE)
        
        # Busca por resultado exitoso/bem-sucedido
        termos_sucesso = ["resultado exitoso", "condução bem-sucedida", "bem-sucedida", 
                          "resultado favorável", "sucesso", "procedente", "favorável"]
        tem_sucesso = any(termo in texto for termo in termos_sucesso)
        
        # Pontuação baseada em critérios encontrados
        pontos = 0
        if tem_defesa: pontos += 1
        if tem_quantidade: pontos += 1
        if len(valores_altos) > 0: pontos += 1
        if tem_tempo: pontos += 1
        if tem_sucesso: pontos += 1
        
        if pontos >= 4:  # Pelo menos 4 dos 5 critérios
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = f"Encontrou evidências de defesas administrativas (5 anos, valores >= 2.500.000, resultado exitoso)"
        elif pontos >= 2:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = f"Menção parcial: encontrou {pontos} de 5 critérios necessários"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou evidências suficientes de 5 defesas administrativas >= 2.500.000 nos últimos 5 anos com resultado exitoso"
    
    def _validate_item_ii(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item ii: 5 processos judiciais >= 2.500.000 nos últimos 5 anos com resultado exitoso"""
        valores = re.findall(r'(?:r\$\s*)?([\d\.]+(?:\.\d{3})*(?:,\d{2})?)', texto, re.IGNORECASE)
        valores_altos = [v for v in valores if self._parse_value(v) >= 2500000]
        
        termos_processo = ["processo judicial", "processos judiciais", "ação judicial", 
                          "ações judiciais", "processo", "processos", "ação", "ações"]
        tem_processo = any(termo in texto for termo in termos_processo)
        
        tem_quantidade = re.search(r'\b(5|cinco|pelo menos 5|mínimo de 5)\b', texto, re.IGNORECASE)
        
        # Busca por "últimos 5 anos"
        tem_tempo = re.search(r'(últimos?\s*5\s*anos?|5\s*anos?|cinco\s*anos?)', texto, re.IGNORECASE)
        
        # Busca por resultado exitoso/bem-sucedido
        termos_sucesso = ["resultado exitoso", "condução bem-sucedida", "bem-sucedida", 
                          "resultado favorável", "sucesso", "procedente", "favorável", "sentença favorável"]
        tem_sucesso = any(termo in texto for termo in termos_sucesso)
        
        # Pontuação baseada em critérios encontrados
        pontos = 0
        if tem_processo: pontos += 1
        if tem_quantidade: pontos += 1
        if len(valores_altos) > 0: pontos += 1
        if tem_tempo: pontos += 1
        if tem_sucesso: pontos += 1
        
        if pontos >= 4:  # Pelo menos 4 dos 5 critérios
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou evidências de processos judiciais (5 anos, valores >= 2.500.000, resultado exitoso)"
        elif pontos >= 2:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = f"Menção parcial: encontrou {pontos} de 5 critérios necessários"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou evidências suficientes de 5 processos judiciais >= 2.500.000 nos últimos 5 anos com resultado exitoso"
    
    def _validate_item_iii(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item iii: Histórico profissional"""
        termos_historico = ["histórico", "histórico profissional", "processos conduzidos", "resultados"]
        tem_historico = any(termo in texto for termo in termos_historico)
        
        termos_area = ["tributária", "tributário", "previdenciária", "previdenciário", "benefício", "custeio"]
        tem_area = any(termo in texto for termo in termos_area)
        
        if tem_historico and tem_area:
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou histórico profissional na área"
        elif tem_historico or tem_area:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = "Menção parcial a histórico profissional"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou histórico profissional completo"
    
    def _validate_item_iv(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item iv: Capacidade contábil"""
        termos_contabil = ["contábil", "contabil", "cpa", "mba", "pós-graduação", "especialização contábil"]
        tem_contabil = any(termo in texto for termo in termos_contabil)
        
        if tem_contabil:
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou menção a formação/especialização contábil"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou comprovação de capacidade contábil"
    
    def _validate_item_i_securitizacao(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item i Lote 2: Defesas administrativas securitização >= 2.500.000 nos últimos 5 anos"""
        valores = re.findall(r'(?:r\$\s*)?([\d\.]+(?:\.\d{3})*(?:,\d{2})?)', texto, re.IGNORECASE)
        valores_altos = [v for v in valores if self._parse_value(v) >= 2500000]
        
        termos_defesa = ["defesa administrativa", "defesas administrativas", "defesa perante", 
                        "receita federal", "receita estadual"]
        termos_securitizacao = ["securitização", "securitizacao", "securitização de créditos", 
                               "securitização de creditos", "créditos", "creditos"]
        
        tem_defesa = any(termo in texto for termo in termos_defesa)
        tem_securitizacao = any(termo in texto for termo in termos_securitizacao)
        tem_quantidade = re.search(r'\b(5|cinco|pelo menos 5|mínimo de 5)\b', texto, re.IGNORECASE)
        
        # Busca por "últimos 5 anos"
        tem_tempo = re.search(r'(últimos?\s*5\s*anos?|5\s*anos?|cinco\s*anos?)', texto, re.IGNORECASE)
        
        # Busca por resultado exitoso
        termos_sucesso = ["resultado exitoso", "condução bem-sucedida", "bem-sucedida", 
                          "resultado favorável", "sucesso", "procedente", "favorável"]
        tem_sucesso = any(termo in texto for termo in termos_sucesso)
        
        pontos = 0
        if tem_defesa: pontos += 1
        if tem_securitizacao: pontos += 1
        if tem_quantidade: pontos += 1
        if len(valores_altos) > 0: pontos += 1
        if tem_tempo: pontos += 1
        if tem_sucesso: pontos += 1
        
        if pontos >= 5:  # Pelo menos 5 dos 6 critérios
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou defesas administrativas em securitização (5 anos, valores >= 2.500.000, resultado exitoso)"
        elif pontos >= 3:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = f"Menção parcial: encontrou {pontos} de 6 critérios necessários"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou evidências suficientes de defesas administrativas em securitização"
    
    def _validate_item_ii_securitizacao(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item ii Lote 2: Processos judiciais securitização >= 2.500.000 nos últimos 5 anos"""
        valores = re.findall(r'(?:r\$\s*)?([\d\.]+(?:\.\d{3})*(?:,\d{2})?)', texto, re.IGNORECASE)
        valores_altos = [v for v in valores if self._parse_value(v) >= 2500000]
        
        termos_processo = ["processo judicial", "processos judiciais", "ação judicial", 
                          "ações judiciais", "processo", "processos"]
        termos_securitizacao = ["securitização", "securitizacao", "securitização de créditos", 
                               "securitização de creditos", "créditos", "creditos"]
        
        tem_processo = any(termo in texto for termo in termos_processo)
        tem_securitizacao = any(termo in texto for termo in termos_securitizacao)
        tem_quantidade = re.search(r'\b(5|cinco|pelo menos 5|mínimo de 5)\b', texto, re.IGNORECASE)
        
        # Busca por "últimos 5 anos"
        tem_tempo = re.search(r'(últimos?\s*5\s*anos?|5\s*anos?|cinco\s*anos?)', texto, re.IGNORECASE)
        
        # Busca por resultado exitoso
        termos_sucesso = ["resultado exitoso", "condução bem-sucedida", "bem-sucedida", 
                          "resultado favorável", "sucesso", "procedente", "favorável", "sentença favorável"]
        tem_sucesso = any(termo in texto for termo in termos_sucesso)
        
        pontos = 0
        if tem_processo: pontos += 1
        if tem_securitizacao: pontos += 1
        if tem_quantidade: pontos += 1
        if len(valores_altos) > 0: pontos += 1
        if tem_tempo: pontos += 1
        if tem_sucesso: pontos += 1
        
        if pontos >= 5:  # Pelo menos 5 dos 6 critérios
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou processos judiciais em securitização (5 anos, valores >= 2.500.000, resultado exitoso)"
        elif pontos >= 3:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = f"Menção parcial: encontrou {pontos} de 6 critérios necessários"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou evidências suficientes de processos judiciais em securitização"
    
    def _validate_item_iii_securitizacao(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item iii Lote 2: Histórico profissional securitização nos últimos 5 anos com valores >= 2.500.000"""
        termos_historico = ["histórico", "histórico profissional", "processos conduzidos", 
                           "lista de processos", "processos realizados"]
        termos_securitizacao = ["securitização", "securitizacao", "securitização de créditos", 
                               "securitização de creditos", "créditos", "creditos"]
        
        valores = re.findall(r'(?:r\$\s*)?([\d\.]+(?:\.\d{3})*(?:,\d{2})?)', texto, re.IGNORECASE)
        valores_altos = [v for v in valores if self._parse_value(v) >= 2500000]
        
        tem_historico = any(termo in texto for termo in termos_historico)
        tem_securitizacao = any(termo in texto for termo in termos_securitizacao)
        tem_tempo = re.search(r'(últimos?\s*5\s*anos?|5\s*anos?|cinco\s*anos?)', texto, re.IGNORECASE)
        tem_resultados = re.search(r'(resultados?|obtidos?|conduzidos?)', texto, re.IGNORECASE)
        
        pontos = 0
        if tem_historico: pontos += 1
        if tem_securitizacao: pontos += 1
        if tem_tempo: pontos += 1
        if len(valores_altos) > 0: pontos += 1
        if tem_resultados: pontos += 1
        
        if pontos >= 4:  # Pelo menos 4 dos 5 critérios
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou histórico profissional em securitização com valores >= 2.500.000 nos últimos 5 anos"
        elif pontos >= 2:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = f"Menção parcial: encontrou {pontos} de 5 critérios necessários"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou histórico profissional completo em securitização"
    
    def _validate_item_iv_securitizacao(self, texto: str, requisito: str, key: str, resultado: Dict):
        """Valida item iv Lote 2: Capacidade contábil securitização e debêntures"""
        termos_contabil = ["contábil", "contabil", "cpa", "mba", "pós-graduação", "pós graduação", 
                           "especialização contábil", "formação contábil", "graduação contábil",
                           "certificado contábil", "curso contábil"]
        termos_securitizacao = ["securitização", "securitizacao", "securitização de créditos", 
                               "securitização de creditos", "créditos", "creditos"]
        termos_debentures = ["debêntures", "debentures", "emissão de debêntures", "emissão de debentures"]
        
        tem_contabil = any(termo in texto for termo in termos_contabil)
        tem_securitizacao = any(termo in texto for termo in termos_securitizacao)
        tem_debentures = any(termo in texto for termo in termos_debentures)
        
        # Verifica se menciona análise de documentos relacionados
        termos_documentos = ["análise de documentos", "análise contábil", "análise fiscal", 
                            "análise financeira", "documentos contábeis", "documentos fiscais"]
        tem_documentos = any(termo in texto for termo in termos_documentos)
        
        pontos = 0
        if tem_contabil: pontos += 1
        if tem_securitizacao: pontos += 1
        if tem_debentures: pontos += 1
        if tem_documentos: pontos += 1
        
        if pontos >= 3:  # Pelo menos 3 dos 4 critérios
            resultado["corretos"].append(key)
            resultado["evidencias"][key] = "Encontrou capacidade contábil para análise de documentos de securitização e debêntures"
        elif pontos >= 2:
            resultado["duvidosos"].append(key)
            resultado["evidencias"][key] = f"Menção parcial: encontrou {pontos} de 4 critérios necessários"
        else:
            resultado["faltando"].append(key)
            resultado["evidencias"][key] = "Não encontrou capacidade contábil completa para análise de documentos de securitização e debêntures"
    
    def _validate_comprovacoes(self, texto: str, resultado: Dict):
        """Valida comprovações obrigatórias"""
        # Sentenças favoráveis
        termos_sentenca = ["sentença", "sentenças", "favorável", "favoráveis", "julgado procedente"]
        tem_sentenca = any(termo in texto for termo in termos_sentenca)
        
        # Certidão de trânsito em julgado
        termos_certidao = ["certidão", "certidao", "trânsito em julgado", "transito em julgado", "trânsito"]
        tem_certidao = any(termo in texto for termo in termos_certidao)
        
        if tem_sentenca and tem_certidao:
            resultado["corretos"].append("comprovacoes")
            resultado["evidencias"]["comprovacoes"] = "Encontrou sentenças favoráveis e certidões de trânsito em julgado"
        elif tem_sentenca or tem_certidao:
            resultado["duvidosos"].append("comprovacoes")
            resultado["evidencias"]["comprovacoes"] = "Encontrou parcialmente comprovações obrigatórias"
        else:
            resultado["faltando"].append("comprovacoes")
            resultado["evidencias"]["comprovacoes"] = "Não encontrou sentenças favoráveis ou certidões de trânsito em julgado"
    
    def _parse_value(self, value_str: str) -> float:
        """Converte string de valor para float (formato brasileiro: 2.500.000,00)"""
        try:
            # Remove espaços e caracteres especiais
            cleaned = value_str.strip().replace("R$", "").replace("r$", "").strip()
            
            # Se tem vírgula, assume formato brasileiro (2.500.000,00)
            if "," in cleaned:
                # Remove pontos (separadores de milhar) e substitui vírgula por ponto
                cleaned = cleaned.replace(".", "").replace(",", ".")
            else:
                # Se não tem vírgula, pode ser formato simples (2500000) ou com pontos (2.500.000)
                # Remove pontos e assume que são separadores de milhar
                cleaned = cleaned.replace(".", "")
            
            return float(cleaned)
        except:
            return 0.0


