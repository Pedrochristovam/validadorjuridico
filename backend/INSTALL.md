# 📦 Instalação Rápida - Validador Jurídico Backend

## Windows

1. **Instale Python 3.9+**
   - Baixe de: https://www.python.org/downloads/
   - Marque "Add Python to PATH" durante instalação

2. **Instale Tesseract OCR**
   - Baixe de: https://github.com/UB-Mannheim/tesseract/wiki
   - Instale e adicione ao PATH do sistema

3. **Execute o setup**
   ```cmd
   cd backend
   setup.bat
   ```

4. **Configure API Key**
   - Edite `backend/.env`
   - Adicione sua `OPENAI_API_KEY` ou `GROQ_API_KEY`

5. **Inicie o servidor**
   ```cmd
   venv\Scripts\activate
   python main.py
   ```

## Linux/macOS

1. **Instale Python 3.9+**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3 python3-venv python3-pip
   
   # macOS
   brew install python3
   ```

2. **Instale Tesseract OCR**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-por
   
   # macOS
   brew install tesseract tesseract-lang
   ```

3. **Execute o setup**
   ```bash
   cd backend
   chmod +x setup.sh
   ./setup.sh
   ```

4. **Configure API Key**
   ```bash
   # Edite o arquivo .env
   nano .env
   # Adicione sua OPENAI_API_KEY ou GROQ_API_KEY
   ```

5. **Inicie o servidor**
   ```bash
   source venv/bin/activate
   python main.py
   ```

## Verificação

Acesse: http://localhost:8000

Você deve ver:
```json
{
  "message": "Validador Jurídico API",
  "version": "1.0.0"
}
```

## Teste Rápido

```bash
# Health check
curl http://localhost:8000/health

# Deve retornar: {"status":"ok"}
```

## Problemas Comuns

**Erro: "Tesseract not found"**
- Verifique se Tesseract está instalado e no PATH
- Windows: Reinicie o terminal após instalar

**Erro: "Module not found"**
- Ative o ambiente virtual: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/macOS)
- Execute: `pip install -r requirements.txt`

**Erro: "API Key not found"**
- Crie arquivo `.env` na pasta `backend/`
- Adicione: `OPENAI_API_KEY=sua-chave-aqui` ou `GROQ_API_KEY=sua-chave-aqui`


