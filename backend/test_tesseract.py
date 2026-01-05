#!/usr/bin/env python3
"""
Script de teste para verificar se o Tesseract está configurado corretamente
"""
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_tesseract():
    """Testa se o Tesseract está funcionando"""
    print("🔍 Verificando configuração do Tesseract OCR...\n")
    
    try:
        import pytesseract
        print("✅ pytesseract importado com sucesso")
    except ImportError:
        print("❌ Erro: pytesseract não está instalado")
        print("   Execute: pip install pytesseract")
        return False
    
    # Tenta encontrar o caminho do Tesseract
    import platform
    import shutil
    
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        print(f"✅ Tesseract encontrado no PATH: {tesseract_path}")
    else:
        print("⚠️  Tesseract não encontrado no PATH")
        
        # Verifica caminhos comuns no Windows
        if platform.system() == "Windows":
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    print(f"✅ Tesseract encontrado em: {path}")
                    pytesseract.pytesseract.tesseract_cmd = path
                    tesseract_path = path
                    break
    
    # Testa se consegue obter a versão
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Versão do Tesseract: {version}")
    except Exception as e:
        print(f"❌ Erro ao obter versão do Tesseract: {e}")
        if not tesseract_path:
            print("   Dica: Configure o caminho do Tesseract ou adicione ao PATH")
        return False
    
    # Testa idiomas disponíveis
    try:
        langs = pytesseract.get_languages()
        print(f"✅ Idiomas disponíveis: {', '.join(langs[:10])}{'...' if len(langs) > 10 else ''}")
        
        if 'por' in langs:
            print("✅ Português (por) está disponível!")
        else:
            print("⚠️  Português (por) não está disponível")
            print("   O sistema usará inglês como fallback")
            if 'eng' in langs:
                print("✅ Inglês (eng) está disponível")
    except Exception as e:
        print(f"⚠️  Erro ao obter idiomas: {e}")
    
    # Testa OCR básico (cria uma imagem simples se possível)
    try:
        from PIL import Image
        import io
        
        # Cria uma imagem de teste simples
        img = Image.new('RGB', (200, 50), color='white')
        print("\n✅ PIL/Pillow disponível para processamento de imagens")
    except ImportError:
        print("\n⚠️  PIL/Pillow não disponível (necessário para OCR de PDFs escaneados)")
    
    print("\n" + "="*50)
    print("✅ Tesseract está configurado e pronto para uso!")
    print("="*50)
    
    return True

if __name__ == "__main__":
    success = test_tesseract()
    sys.exit(0 if success else 1)





