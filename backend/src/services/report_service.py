"""
Serviço para gerar relatório PDF
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ReportService:
    """Gera relatórios PDF de validação"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos customizados - versão simplificada"""
        # Estilos básicos sem formatação complexa
        pass
    
    def generate_report(self, resultado: Dict, output_path: Path) -> Path:
        """
        Gera relatório PDF com os resultados da validação
        """
        try:
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Título - versão simples sem formatação complexa
            story.append(Paragraph("Relatório de Validação de Documento Jurídico", self.styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            # Data
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            story.append(Paragraph(f"Gerado em: {data_atual}", self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Status Geral - versão simples
            status = resultado.get("status_geral", "REPROVADO")
            story.append(Paragraph(f"STATUS: {status}", self.styles['Heading2']))
            story.append(Spacer(1, 0.3*inch))
            
            # Requisitos Corretos - versão simples sem formatação
            corretos = resultado.get("corretos", [])
            if corretos:
                story.append(Paragraph("Requisitos Atendidos", self.styles['Heading2']))
                for idx, item in enumerate(corretos, 1):
                    # Limpa texto e garante que tudo seja incluído
                    item_text = str(item) if item else ""
                    # Remove apenas caracteres que podem quebrar o PDF, mantém o conteúdo
                    item_clean = item_text.replace('<', '').replace('>', '').replace('&', 'e').strip()
                    if item_clean:  # Só adiciona se não estiver vazio
                        story.append(Paragraph(f"{idx}. {item_clean}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Requisitos Faltando - versão simples sem formatação
            faltando = resultado.get("faltando", [])
            if faltando:
                story.append(Paragraph("Requisitos Não Comprovados", self.styles['Heading2']))
                for idx, item in enumerate(faltando, 1):
                    item_text = str(item) if item else ""
                    item_clean = item_text.replace('<', '').replace('>', '').replace('&', 'e').strip()
                    if item_clean:
                        story.append(Paragraph(f"{idx}. {item_clean}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Requisitos Duvidosos - versão simples sem formatação
            duvidosos = resultado.get("duvidosos", [])
            if duvidosos:
                story.append(Paragraph("Requisitos Parcialmente Comprovados", self.styles['Heading2']))
                for idx, item in enumerate(duvidosos, 1):
                    item_text = str(item) if item else ""
                    item_clean = item_text.replace('<', '').replace('>', '').replace('&', 'e').strip()
                    if item_clean:
                        story.append(Paragraph(f"{idx}. {item_clean}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Evidências - versão simples sem formatação, garantindo todo conteúdo
            evidencias = resultado.get("evidencias", {})
            if evidencias:
                story.append(PageBreak())
                story.append(Paragraph("Evidências Encontradas", self.styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                
                for requisito, evidencia in evidencias.items():
                    req_text = str(requisito) if requisito else ""
                    evid_text = str(evidencia) if evidencia else ""
                    
                    req_clean = req_text.replace('<', '').replace('>', '').replace('&', 'e').strip()
                    evid_clean = evid_text.replace('<', '').replace('>', '').replace('&', 'e').strip()
                    
                    if req_clean:
                        story.append(Paragraph(f"Requisito: {req_clean}", self.styles['Normal']))
                    if evid_clean:
                        # Quebra evidências longas em múltiplos parágrafos se necessário
                        evid_lines = evid_clean.split('\n')
                        for line in evid_lines:
                            line_clean = line.strip()
                            if line_clean:
                                story.append(Paragraph(line_clean, self.styles['Normal']))
                    story.append(Spacer(1, 0.15*inch))
            
            # Resumo em tabela - versão simples sem formatação complexa
            story.append(PageBreak())
            story.append(Paragraph("Resumo da Validação", self.styles['Heading2']))
            
            data_table = [
                ['Categoria', 'Quantidade'],
                ['Requisitos Atendidos', str(len(corretos))],
                ['Requisitos Não Comprovados', str(len(faltando))],
                ['Requisitos Parcialmente Comprovados', str(len(duvidosos))],
                ['Status Final', status]
            ]
            
            # Tabela simples sem formatação complexa
            table = Table(data_table, colWidths=[4*inch, 2*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            
            # Gera PDF
            doc.build(story)
            logger.info(f"Relatório PDF gerado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório PDF: {e}")
            raise Exception(f"Erro ao gerar relatório: {str(e)}")


