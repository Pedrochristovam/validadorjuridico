# 🚀 Configurar Frontend no Render

## Problema Atual
O backend está funcionando no Render, mas o frontend não está aparecendo. Isso acontece porque o frontend precisa ser deployado separadamente.

## Solução: Deploy do Frontend no Render

### Opção 1: Deploy como Static Site (Recomendado)

1. **No Dashboard do Render:**
   - Vá em "New" → "Static Site"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name:** `validador-juridico-frontend`
     - **Build Command:** `npm install && npm run build`
     - **Publish Directory:** `dist`
     - **Environment Variables:**
       - `VITE_API_URL` = `https://validadorjuridico.onrender.com/api`

2. **Após o deploy:**
   - O Render vai gerar uma URL para o frontend (ex: `validador-juridico-frontend.onrender.com`)
   - Atualize a variável `CORS_ORIGINS` no backend para incluir essa URL

### Opção 2: Usar o render.yaml (Já configurado)

O arquivo `render.yaml` já está configurado. Para usar:

1. **No Dashboard do Render:**
   - Vá em "New" → "Blueprint"
   - Conecte seu repositório GitHub
   - O Render vai detectar o `render.yaml` automaticamente

2. **Configure as variáveis de ambiente:**
   - **Backend (`validador-juridico-api`):**
     - `CORS_ORIGINS` = URL do frontend (será gerada após deploy)
   - **Frontend (`validador-juridico-frontend`):**
     - `VITE_API_URL` = `https://validadorjuridico.onrender.com/api`

## ⚠️ Importante

O frontend precisa saber qual é a URL do backend. O código já está configurado para:
- Usar `VITE_API_URL` se estiver definida
- Detectar automaticamente se está em produção e usar `https://validadorjuridico.onrender.com/api`
- Usar `http://localhost:8000/api` apenas em desenvolvimento local

## 📝 Passos Rápidos

1. **Deploy do Frontend:**
   ```
   Render Dashboard → New → Static Site
   → Conecte GitHub
   → Build: npm install && npm run build
   → Publish: dist
   → Env Var: VITE_API_URL=https://validadorjuridico.onrender.com/api
   ```

2. **Atualizar CORS no Backend:**
   ```
   Backend Dashboard → Environment Variables
   → CORS_ORIGINS = https://validador-juridico-frontend.onrender.com
   ```

3. **Pronto!** O frontend vai aparecer funcionando.

