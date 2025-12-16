# 🚀 Como Iniciar o Sistema

## ⚠️ IMPORTANTE: O Backend precisa estar rodando!

O erro "Failed to fetch" acontece quando o backend não está rodando.

## 📋 Passo a Passo para Iniciar

### 1. Iniciar o Backend (Terminal 1)

```bash
cd backend
py main.py
```

Ou se `python` funcionar:
```bash
cd backend
python main.py
```

**Você deve ver:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Iniciar o Frontend (Terminal 2)

```bash
npm run dev
```

**Você deve ver:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

## ✅ Verificar se está funcionando

1. **Backend**: Acesse http://localhost:8000/health
   - Deve retornar: `{"status":"ok"}`

2. **Frontend**: Acesse http://localhost:5173
   - Deve carregar a página normalmente

## 🐛 Se ainda der erro "Failed to fetch"

1. **Verifique se o backend está rodando:**
   - Abra http://localhost:8000/health no navegador
   - Se não abrir, o backend não está rodando

2. **Verifique a porta:**
   - Backend deve estar na porta 8000
   - Frontend deve estar na porta 5173 ou 5174

3. **Verifique o console do navegador (F12):**
   - Veja se há erros de CORS
   - Veja a URL exata que está tentando acessar

4. **Reinicie ambos os servidores:**
   - Pare o backend (Ctrl+C)
   - Pare o frontend (Ctrl+C)
   - Inicie novamente

## 📝 Notas

- **Windows**: Use `py` ao invés de `python` se `python` não funcionar
- **Ambiente Virtual**: Se estiver usando venv, ative antes: `.\env\Scripts\activate`
- **Portas**: Se a porta 8000 estiver ocupada, altere no `main.py` ou use outra porta

