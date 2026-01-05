# 🚀 Guia de Deploy no Render

Este guia explica como fazer o deploy do Validador Jurídico no Render.

## 📋 Pré-requisitos

1. Conta no [Render](https://render.com)
2. Repositório Git (GitHub, GitLab ou Bitbucket)
3. API Keys configuradas (OpenAI ou Groq)

## 🔧 Configuração do Backend

### 1. Criar Novo Web Service

1. Acesse o [Dashboard do Render](https://dashboard.render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório Git
4. Configure:
   - **Name**: `validador-juridico-api`
   - **Region**: `São Paulo` (ou mais próximo)
   - **Branch**: `main` (ou sua branch principal)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### 2. Variáveis de Ambiente (Backend)

Configure as seguintes variáveis no dashboard do Render:

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `PORT` | `8000` | Porta do servidor (Render define automaticamente) |
| `ENVIRONMENT` | `production` | Ambiente de produção |
| `AI_PROVIDER` | `openai` ou `groq` | Provedor de IA |
| `OPENAI_API_KEY` | `sua-chave-aqui` | Chave da API OpenAI (se usar OpenAI) |
| `GROQ_API_KEY` | `sua-chave-aqui` | Chave da API Groq (se usar Groq) |
| `CORS_ORIGINS` | `https://seu-frontend.onrender.com` | URL do frontend (configure após deploy) |

### 3. Buildpacks e Dependências

O Render detecta automaticamente Python. Certifique-se de que:
- O arquivo `requirements.txt` está no diretório `backend/`
- O arquivo `main.py` está no diretório `backend/`

## 🎨 Configuração do Frontend

### 1. Criar Novo Static Site

1. No Dashboard do Render, clique em **"New +"** → **"Static Site"**
2. Conecte seu repositório Git
3. Configure:
   - **Name**: `validador-juridico-frontend`
   - **Branch**: `main` (ou sua branch principal)
   - **Root Directory**: `.` (raiz do projeto)
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

### 2. Variáveis de Ambiente (Frontend)

Configure a seguinte variável:

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `VITE_API_URL` | `https://seu-backend.onrender.com/api` | URL completa da API backend |

**⚠️ Importante**: Substitua `seu-backend.onrender.com` pela URL real do seu backend após o deploy.

## 📝 Passo a Passo Completo

### Passo 1: Deploy do Backend

1. Faça push do código para o Git
2. Crie o Web Service no Render conforme instruções acima
3. Configure as variáveis de ambiente
4. Aguarde o build e deploy
5. Anote a URL do backend (ex: `https://validador-juridico-api.onrender.com`)

### Passo 2: Atualizar CORS do Backend

1. No dashboard do backend, vá em **Environment**
2. Adicione/atualize a variável `CORS_ORIGINS`:
   ```
   https://validador-juridico-frontend.onrender.com
   ```
   (Use a URL que você vai obter no próximo passo)

### Passo 3: Deploy do Frontend

1. Crie o Static Site conforme instruções acima
2. Configure a variável `VITE_API_URL` com a URL do backend:
   ```
   https://validador-juridico-api.onrender.com/api
   ```
3. Aguarde o build e deploy
4. Anote a URL do frontend (ex: `https://validador-juridico-frontend.onrender.com`)

### Passo 4: Atualizar CORS (Novamente)

1. Volte ao dashboard do backend
2. Atualize `CORS_ORIGINS` com a URL real do frontend:
   ```
   https://validador-juridico-frontend.onrender.com
   ```
3. Faça um redeploy ou aguarde alguns minutos

## 🔍 Verificação

1. Acesse a URL do frontend
2. Abra o Console do navegador (F12)
3. Verifique se não há erros de CORS
4. Teste fazer upload de um documento

## ⚠️ Limitações do Plano Gratuito

- **Sleep após inatividade**: Serviços gratuitos "dormem" após 15 minutos de inatividade
- **Primeira requisição lenta**: Após dormir, a primeira requisição pode levar alguns segundos
- **Limite de recursos**: CPU e memória limitados

## 🐛 Troubleshooting

### Erro de CORS

**Sintoma**: Erro no console do navegador sobre CORS

**Solução**:
1. Verifique se `CORS_ORIGINS` está configurado corretamente no backend
2. Certifique-se de incluir a URL completa do frontend (com `https://`)
3. Faça um redeploy do backend após alterar variáveis

### Backend não inicia

**Sintoma**: Build falha ou serviço não inicia

**Solução**:
1. Verifique os logs no dashboard do Render
2. Certifique-se de que `requirements.txt` está correto
3. Verifique se todas as variáveis de ambiente estão configuradas

### Frontend não encontra API

**Sintoma**: Erro 404 ou "Failed to fetch"

**Solução**:
1. Verifique se `VITE_API_URL` está configurada corretamente
2. Certifique-se de incluir `/api` no final da URL
3. Verifique se o backend está rodando (acesse `/health` no navegador)

### Tesseract não encontrado

**Sintoma**: Erro ao processar PDFs escaneados

**Solução**:
- O Render não suporta Tesseract diretamente no plano gratuito
- Considere usar um serviço externo de OCR ou upgrade para um plano pago
- Alternativamente, processe OCR localmente antes de enviar

## 📚 Recursos Adicionais

- [Documentação do Render](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-python)
- [Render Static Sites](https://render.com/docs/static-sites)

## 💡 Dicas

1. **Domínios customizados**: Você pode adicionar um domínio customizado no Render
2. **Auto-deploy**: Por padrão, o Render faz deploy automático a cada push
3. **Logs**: Use o dashboard para ver logs em tempo real
4. **Health Checks**: O backend tem um endpoint `/health` para verificação





