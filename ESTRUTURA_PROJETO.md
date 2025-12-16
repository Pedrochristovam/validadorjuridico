# 📁 Estrutura Completa do Projeto - Validador Jurídico

## 🗂️ Visão Geral da Estrutura

```
validador-juridico/
│
├── 📂 backend/                    # API FastAPI (Python)
│   ├── 📄 main.py                 # Ponto de entrada da API
│   ├── 📄 run.py                  # Script alternativo de execução
│   ├── 📄 requirements.txt        # Dependências Python
│   ├── 📄 runtime.txt            # Versão Python (3.11.0)
│   ├── 📄 modelo.json            # Modelo padrão de validação
│   ├── 📄 env.example.txt        # Exemplo de variáveis de ambiente
│   ├── 📄 setup.bat               # Script de setup (Windows)
│   ├── 📄 setup.sh               # Script de setup (Linux/macOS)
│   ├── 📄 start.bat               # Script de start produção (Windows)
│   ├── 📄 start.sh               # Script de start produção (Linux)
│   ├── 📄 test_tesseract.py      # Teste do Tesseract OCR
│   ├── 📄 README.md               # Documentação do backend
│   ├── 📄 INSTALL.md              # Guia de instalação
│   │
│   ├── 📂 src/                    # Código fonte do backend
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📂 routes/             # Rotas da API
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 upload_routes.py      # Rotas de upload
│   │   │   └── 📄 validation_routes.py  # Rotas de validação
│   │   │
│   │   ├── 📂 controllers/        # Controllers (lógica de controle)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 upload_controller.py      # Controller de upload
│   │   │   └── 📄 validation_controller.py  # Controller de validação
│   │   │
│   │   ├── 📂 services/           # Serviços (lógica de negócio)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 extraction_service.py    # Extração de texto
│   │   │   ├── 📄 ocr_service.py            # Serviço OCR (Tesseract)
│   │   │   ├── 📄 rule_validator.py         # Validação por regras
│   │   │   ├── 📄 ai_validator.py           # Validação com IA
│   │   │   ├── 📄 validation_service.py     # Serviço principal de validação
│   │   │   └── 📄 report_service.py        # Geração de relatórios PDF
│   │   │
│   │   ├── 📂 models/             # Schemas Pydantic
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 schemas.py      # Modelos de dados
│   │   │
│   │   └── 📂 utils/              # Utilitários
│   │       ├── 📄 __init__.py
│   │       └── 📄 file_handler.py # Manipulação de arquivos
│   │
│   ├── 📂 uploads/                # Arquivos enviados (criado automaticamente)
│   ├── 📂 reports/                # Relatórios gerados (criado automaticamente)
│   └── 📂 modelos/                # Modelos salvos (criado automaticamente)
│       └── 📄 .gitkeep            # Mantém diretório no Git
│
├── 📂 src/                        # Frontend React (código fonte principal)
│   ├── 📄 main.jsx                # Ponto de entrada React
│   ├── 📄 App.jsx                 # Componente raiz com rotas
│   ├── 📄 Layout.jsx              # Layout principal com navegação
│   ├── 📄 index.css               # Estilos globais
│   ├── 📄 utils.js                # Funções utilitárias
│   │
│   ├── 📂 api/                    # Cliente API
│   │   └── 📄 apiClient.js        # Cliente para comunicação com backend
│   │
│   ├── 📂 Pages/                  # Páginas da aplicação
│   │   ├── 📄 Home.jsx            # Página principal (upload/validação)
│   │   ├── 📄 Models.jsx          # Página de gerenciamento de modelos
│   │   └── 📄 History.jsx         # Página de histórico de validações
│   │
│   ├── 📂 components/             # Componentes React
│   │   ├── 📂 ui/                 # Componentes UI reutilizáveis
│   │   │   ├── 📄 button.jsx      # Botão
│   │   │   ├── 📄 card.jsx        # Card
│   │   │   ├── 📄 input.jsx       # Input
│   │   │   ├── 📄 select.jsx      # Select/Dropdown
│   │   │   ├── 📄 badge.jsx       # Badge
│   │   │   └── 📄 checkbox.jsx    # Checkbox
│   │   │
│   │   ├── 📂 upload/             # Componentes de upload
│   │   │   └── 📄 DropZone.jsx    # Zona de arrastar/soltar arquivos
│   │   │
│   │   ├── 📂 validation/         # Componentes de validação
│   │   │   └── 📄 ValidationResults.jsx  # Exibição de resultados
│   │   │
│   │   ├── 📂 models/             # Componentes de modelos
│   │   │   └── 📄 FieldsConfig.jsx       # Configuração de campos
│   │   │
│   │   └── 📄 UserNotRegisteredError.jsx  # Componente de erro
│   │
│   └── 📂 lib/                    # Bibliotecas auxiliares
│       └── 📄 utils.js            # Utilitários (clsx, tailwind-merge)
│
├── 📂 Components/                 # Componentes legados (duplicados)
│   ├── 📂 models/
│   ├── 📂 upload/
│   ├── 📂 validation/
│   └── 📄 UserNotRegisteredError.jsx
│
├── 📂 Pages/                      # Páginas legadas (duplicadas)
│   ├── 📄 Home.jsx
│   ├── 📄 Models.jsx
│   └── 📄 History.jsx
│
├── 📂 Entities/                   # Entidades JSON (legado)
│   ├── 📄 DocumentModel.json
│   └── 📄 ValidationResult.json
│
├── 📄 index.html                   # HTML principal
├── 📄 package.json                # Dependências Node.js
├── 📄 package-lock.json           # Lock file do npm
├── 📄 vite.config.js              # Configuração do Vite
├── 📄 tailwind.config.js          # Configuração do Tailwind CSS
├── 📄 postcss.config.js           # Configuração do PostCSS
├── 📄 README.md                   # Documentação principal
├── 📄 RENDER_DEPLOY.md            # Guia de deploy no Render
├── 📄 render.yaml                 # Configuração do Render (opcional)
├── 📄 .gitignore                  # Arquivos ignorados pelo Git
├── 📄 Layout.js                   # Layout legado
├── 📄 utils.js                    # Utilitários legados
└── 📄 FLUXO_SISTEMA.md            # Documentação do fluxo do sistema
```

---

## 📋 Descrição dos Diretórios Principais

### 🔷 Backend (`backend/`)

**Arquivos de Configuração:**
- `main.py` - Aplicação FastAPI principal
- `requirements.txt` - Dependências Python
- `runtime.txt` - Versão Python (3.11.0)
- `env.example.txt` - Exemplo de variáveis de ambiente

**Estrutura de Código (`backend/src/`):**
- **routes/** - Define endpoints da API
- **controllers/** - Orquestra requisições e respostas
- **services/** - Lógica de negócio (OCR, validação, IA)
- **models/** - Schemas de dados (Pydantic)
- **utils/** - Funções auxiliares

**Diretórios de Dados:**
- `uploads/` - Arquivos enviados pelos usuários
- `reports/` - Relatórios PDF gerados
- `modelos/` - Modelos de documento salvos

### 🎨 Frontend (`src/`)

**Estrutura Principal:**
- `main.jsx` - Ponto de entrada da aplicação React
- `App.jsx` - Configuração de rotas
- `Layout.jsx` - Layout com navegação

**Organização:**
- **api/** - Cliente HTTP para backend
- **Pages/** - Páginas principais da aplicação
- **components/** - Componentes reutilizáveis
  - **ui/** - Componentes de interface básicos
  - **upload/** - Componentes de upload
  - **validation/** - Componentes de validação
  - **models/** - Componentes de modelos

**Configurações:**
- `vite.config.js` - Configuração do Vite
- `tailwind.config.js` - Configuração do Tailwind
- `package.json` - Dependências e scripts

---

## 🔗 Fluxo de Dados

```
Frontend (React)
    ↓
apiClient.js (src/api/)
    ↓ HTTP Requests
Backend (FastAPI)
    ↓
Routes (src/routes/)
    ↓
Controllers (src/controllers/)
    ↓
Services (src/services/)
    ├── extraction_service.py (extrai texto)
    ├── ocr_service.py (OCR para PDFs escaneados)
    ├── rule_validator.py (validação programada)
    ├── ai_validator.py (validação com IA)
    └── validation_service.py (orquestra validação)
```

---

## 📦 Dependências Principais

### Backend (Python)
- FastAPI - Framework web
- Uvicorn - Servidor ASGI
- Tesseract OCR - Extração de texto de imagens
- OpenAI/Groq - Validação com IA
- PDF/DOCX libraries - Processamento de documentos

### Frontend (Node.js)
- React 18 - Biblioteca UI
- Vite - Build tool
- React Router - Roteamento
- TanStack Query - Gerenciamento de estado servidor
- Tailwind CSS - Estilização
- Framer Motion - Animações

---

## 🚀 Arquivos de Deploy

- `render.yaml` - Configuração do Render (opcional)
- `RENDER_DEPLOY.md` - Guia completo de deploy
- `backend/start.sh` - Script de start (Linux)
- `backend/start.bat` - Script de start (Windows)
- `.gitignore` - Arquivos ignorados pelo Git

---

## ⚠️ Notas Importantes

1. **Duplicação**: Existem arquivos duplicados em `Components/` e `Pages/` (legado). O código ativo está em `src/`.

2. **Diretórios Criados Automaticamente**: `uploads/`, `reports/`, `modelos/` são criados automaticamente pelo backend.

3. **Arquivos de Build**: `node_modules/`, `dist/`, `__pycache__/` são ignorados pelo Git.

4. **Variáveis de Ambiente**: Use `backend/env.example.txt` como referência.

---

## 📊 Estatísticas do Projeto

- **Backend**: ~15 arquivos Python principais
- **Frontend**: ~20 componentes React
- **Páginas**: 3 páginas principais (Home, Models, History)
- **Endpoints API**: 6 endpoints principais
- **Serviços**: 6 serviços principais

---

*Última atualização: Estrutura atual do projeto Validador Jurídico*

