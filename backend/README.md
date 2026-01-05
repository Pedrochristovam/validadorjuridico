# Validador Jurídico - Backend

Sistema de validação automática de documentos jurídicos usando Python + FastAPI.

## 🚀 Instalação Rápida

### 1. Pré-requisitos

- Python 3.9+
- Tesseract OCR instalado no sistema

**Windows:**
```bash
# Baixe e instale Tesseract de: https://github.com/UB-Mannheim/tesseract/wiki
# Adicione ao PATH ou configure variável de ambiente
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### 2. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite .env e adicione sua API key
# Escolha: OPENAI_API_KEY ou GROQ_API_KEY
```

### 4. Executar Servidor

```bash
python main.py
```

Ou com uvicorn diretamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: `http://localhost:8000`

## 📋 Endpoints

### POST `/api/uploadDocumento`
Upload de documento (PDF ou DOCX) e extração de texto.

**Request:**
- `file`: Arquivo PDF ou DOCX (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "message": "Documento processado com sucesso",
  "texto_extraido": "...",
  "filename": "documento.pdf"
}
```

### POST `/api/uploadModelo`
Upload e salvamento do modelo oficial.

**Request:**
```json
{
  "modelo": "Qualificação Técnica – Escritórios Associados",
  "requisitos": { ... }
}
```

### POST `/api/validar`
Valida documento contra modelo oficial.

**Request:**
```json
{
  "texto_documento": "texto extraído do documento...",
  "modelo_id": "default",
  "use_ai": true
}
```

**Response:**
```json
{
  "corretos": ["requisito1", "requisito2"],
  "faltando": ["requisito3"],
  "duvidosos": ["requisito4"],
  "evidencias": {
    "requisito1": "evidência encontrada..."
  },
  "status_geral": "APROVADO"
}
```

### POST `/api/validar/relatorio`
Valida documento e retorna relatório PDF.

## 🏗️ Estrutura do Projeto

```
backend/
├── src/
│   ├── routes/          # Rotas da API
│   ├── controllers/     # Controllers
│   ├── services/        # Lógica de negócio
│   │   ├── extraction_service.py    # Extração de texto
│   │   ├── rule_validator.py        # Validação programada
│   │   ├── ai_validator.py          # Validação com IA
│   │   ├── validation_service.py    # Serviço principal
│   │   └── report_service.py        # Geração de PDF
│   ├── models/          # Schemas Pydantic
│   └── utils/           # Utilitários
├── modelo.json          # Modelo oficial
├── main.py              # Aplicação FastAPI
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## 🔧 Configuração

### Provider de IA

O sistema suporta:
- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Groq** (Llama 3.1, Mixtral)

Configure no `.env`:
```env
AI_PROVIDER=openai  # ou groq
OPENAI_API_KEY=sua-chave-aqui
```

### Desabilitar IA

Para usar apenas validação programada:
```json
{
  "texto_documento": "...",
  "use_ai": false
}
```

## 📝 Notas

- PDFs escaneados são processados automaticamente com OCR (Tesseract)
- O modelo oficial está em `modelo.json`
- Relatórios PDF são salvos em `reports/`
- Arquivos enviados são salvos em `uploads/`

## 🐛 Troubleshooting

**Erro ao processar PDF:**
- Verifique se Tesseract está instalado
- Verifique se o PDF não está corrompido

**Erro de API Key:**
- Verifique se `.env` está configurado corretamente
- Verifique se a API key é válida

**Erro de importação:**
- Execute `pip install -r requirements.txt` novamente
- Verifique se está usando Python 3.9+

## 📄 Licença

Uso interno.







