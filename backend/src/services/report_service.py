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
        """Configura estilos customizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='StatusAprovado',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.green,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='StatusReprovado',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.red,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
    
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
            
            # Título
            story.append(Paragraph("Relatório de Validação de Documento Jurídico", self.styles['CustomTitle']))
            story.append(Spacer(1, 0.2*inch))
            
            # Data
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            story.append(Paragraph(f"<i>Gerado em: {data_atual}</i>", self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Status Geral
            status = resultado.get("status_geral", "REPROVADO")
            if status == "APROVADO":
                story.append(Paragraph(f"<b>STATUS: {status}</b>", self.styles['StatusAprovado']))
            else:
                story.append(Paragraph(f"<b>STATUS: {status}</b>", self.styles['StatusReprovado']))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Requisitos Corretos
            corretos = resultado.get("corretos", [])
            if corretos:
                story.append(Paragraph("✓ Requisitos Atendidos", self.styles['CustomHeading']))
                for item in corretos:
                    story.append(Paragraph(f"• {item}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Requisitos Faltando
            faltando = resultado.get("faltando", [])
            if faltando:
                story.append(Paragraph("✗ Requisitos Não Comprovados", self.styles['CustomHeading']))
                for item in faltando:
                    story.append(Paragraph(f"• {item}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Requisitos Duvidosos
            duvidosos = resultado.get("duvidosos", [])
            if duvidosos:
                story.append(Paragraph("⚠ Requisitos Parcialmente Comprovados", self.styles['CustomHeading']))
                for item in duvidosos:
                    story.append(Paragraph(f"• {item}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Evidências
            evidencias = resultado.get("evidencias", {})
            if evidencias:
                story.append(PageBreak())
                story.append(Paragraph("Evidências Encontradas", self.styles['CustomHeading']))
                
                for requisito, evidencia in evidencias.items():
                    story.append(Paragraph(f"<b>{requisito}:</b>", self.styles['Normal']))
                    story.append(Paragraph(evidencia, self.styles['Normal']))
                    story.append(Spacer(1, 0.15*inch))
            
            # Resumo em tabela
            story.append(PageBreak())
            story.append(Paragraph("Resumo da Validação", self.styles['CustomHeading']))
            
            data_table = [
                ['Categoria', 'Quantidade'],
                ['Requisitos Atendidos', str(len(corretos))],
                ['Requisitos Não Comprovados', str(len(faltando))],
                ['Requisitos Parcialmente Comprovados', str(len(duvidosos))],
                ['Status Final', status]
            ]
            
            table = Table(data_table, colWidths=[4*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
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


