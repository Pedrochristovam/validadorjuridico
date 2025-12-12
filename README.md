# Validador Jurídico

Sistema de validação automática de documentos jurídicos usando IA e OCR (Tesseract).

## 🚀 Como iniciar o projeto

### Pré-requisitos

- Node.js 18+ e npm
- Python 3.9+
- Tesseract OCR instalado

### 1. Backend

```bash
cd backend

# Instalar dependências Python
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example.txt .env
# Edite .env e adicione suas API keys (OPENAI_API_KEY ou GROQ_API_KEY)

# Iniciar servidor
python main.py
```

O backend estará disponível em `http://localhost:8000`

### 2. Frontend

```bash
# Instalar dependências
npm install

# Configurar variáveis de ambiente (opcional para desenvolvimento)
# Crie um arquivo .env.local com:
# VITE_API_URL=http://localhost:8000/api

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## 📁 Estrutura do Projeto

```
├── backend/
│   ├── src/
│   │   ├── routes/          # Rotas da API FastAPI
│   │   ├── controllers/     # Controllers
│   │   ├── services/        # Lógica de negócio (OCR, validação, IA)
│   │   ├── models/          # Schemas Pydantic
│   │   └── utils/           # Utilitários
│   ├── modelo.json          # Modelo oficial de validação
│   ├── modelos/             # Modelos salvos pelos usuários
│   ├── uploads/             # Arquivos enviados
│   └── reports/             # Relatórios gerados
│
└── src/
    ├── api/
    │   └── apiClient.js      # Cliente API para comunicação com backend
    ├── components/
    │   ├── ui/               # Componentes UI reutilizáveis
    │   ├── upload/           # Componente de upload
    │   ├── validation/       # Componente de resultados
    │   └── models/           # Componente de configuração de campos
    ├── Pages/
    │   ├── Home.jsx          # Página principal de validação
    │   ├── Models.jsx        # Página de modelos
    │   └── History.jsx        # Página de histórico
    ├── Layout.jsx            # Layout principal com navegação
    ├── App.jsx               # Componente raiz com rotas
    └── main.jsx              # Ponto de entrada
```

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web Python
- **Tesseract OCR** - Extração de texto de imagens/PDFs
- **OpenAI/Groq** - Validação com IA
- **Pydantic** - Validação de dados

### Frontend
- **React 18** - Biblioteca UI
- **Vite** - Build tool
- **React Router** - Roteamento
- **TanStack Query** - Gerenciamento de estado servidor
- **Framer Motion** - Animações
- **Tailwind CSS** - Estilização
- **Lucide React** - Ícones

## 📋 Funcionalidades

- ✅ Upload de documentos (PDF, DOCX)
- ✅ Extração automática de texto com OCR (Tesseract)
- ✅ Validação baseada em regras programadas
- ✅ Validação com IA (OpenAI/Groq)
- ✅ Gerenciamento de modelos de documento
- ✅ Histórico de validações
- ✅ Relatórios em PDF

## 🔧 Configuração

### Tesseract OCR

**Windows:**
- Baixe e instale de: https://github.com/UB-Mannheim/tesseract/wiki
- Adicione ao PATH ou configure variável de ambiente

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### Variáveis de Ambiente

#### Backend (`backend/.env`)

```env
AI_PROVIDER=openai  # ou groq
OPENAI_API_KEY=sua-chave-aqui
# ou
GROQ_API_KEY=sua-chave-aqui
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=*
```

#### Frontend (`.env.local` - opcional)

```env
VITE_API_URL=http://localhost:8000/api
```

## 🚀 Deploy no Render

Para fazer deploy no Render, consulte o guia completo em [RENDER_DEPLOY.md](./RENDER_DEPLOY.md)

### Resumo rápido:

1. **Backend**: Crie um Web Service no Render
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

2. **Frontend**: Crie um Static Site no Render
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

3. Configure as variáveis de ambiente conforme `RENDER_DEPLOY.md`

## 📝 Notas

- O sistema usa Tesseract OCR para extrair texto de PDFs escaneados
- A validação pode ser feita com regras programadas ou com IA
- Modelos de documento podem ser salvos e reutilizados
- Consulte `backend/README.md` para mais detalhes sobre a API

## 📄 Licença

Uso interno.
