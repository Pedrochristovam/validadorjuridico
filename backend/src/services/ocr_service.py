import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import docx
import os
import platform
import shutil

# Detecção automática do caminho do Tesseract
def _find_tesseract():
    """Encontra o caminho do Tesseract automaticamente"""
    # Verifica se já está no PATH
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        return tesseract_path
    
    # Caminhos comuns no Windows
    if platform.system() == "Windows":
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv("USERNAME", "")),
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
    
    # Linux/macOS - geralmente está no PATH, mas tenta alguns caminhos comuns
    elif platform.system() in ["Linux", "Darwin"]:
        common_paths = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",  # macOS Apple Silicon
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
    
    # Se não encontrou, retorna None e o pytesseract tentará usar o PATH
    return None

# Configura o caminho do Tesseract se encontrado
tesseract_path = _find_tesseract()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_pdf(path):
    """Extrai texto de PDF (combina pdfplumber e Tesseract)."""
    # Tenta extrair texto direto (PDF digital)
    try:
        with pdfplumber.open(path) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        text = "\n".join(pages).strip()
        if text and len(text) > 50:  # Se extraiu texto suficiente, retorna
            return text
    except Exception:
        pass

    # Se for PDF escaneado (imagem), usa Tesseract
    try:
        images = convert_from_path(path, dpi=300)
        text_pages = []
        # Tenta usar português, se não disponível usa inglês
        lang = 'por+eng'  # Português + Inglês como fallback
        try:
            # Verifica se o idioma português está disponível
            available_langs = pytesseract.get_languages()
            if 'por' not in available_langs:
                lang = 'eng'  # Se português não disponível, usa inglês
        except Exception:
            lang = 'eng'  # Se houver erro, usa inglês
        
        for img in images:
            try:
                text_page = pytesseract.image_to_string(img, lang=lang)
                text_pages.append(text_page)
            except Exception:
                # Se falhar em uma página, continua com as outras
                continue
        
        result = "\n".join(text_pages).strip()
        return result if result else ""
    except Exception as e:
        # Se falhar o OCR completamente, retorna string vazia
        # Log do erro pode ser adicionado aqui se necessário
        return ""


def extract_text_docx(path):
    """Extrai texto de arquivos .docx"""
    d = docx.Document(path)
    return "\n".join([p.text for p in d.paragraphs])
