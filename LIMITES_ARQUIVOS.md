# 📄 Limites de Tamanho de Arquivo - Validador Jurídico

## 📋 Visão Geral

O sistema possui **limites configuráveis** de tamanho de arquivo para garantir performance e estabilidade. Os limites podem ser ajustados conforme suas necessidades.

## ⚙️ Limites Padrão

| Tipo de Arquivo | Limite Padrão | Configurável Via |
|----------------|---------------|------------------|
| **Documentos para validação** | 50MB | `MAX_FILE_SIZE_DOCUMENTO` |
| **Modelos de documento** | 20MB | `MAX_FILE_SIZE_MODELO` |
| **Upload geral (FastAPI)** | 100MB | `MAX_UPLOAD_SIZE` |

## 🔧 Como Configurar os Limites

### 1. Via Variáveis de Ambiente

Edite o arquivo `.env` no diretório `backend/` ou configure no Render:

```env
# Limites em bytes
# 50MB = 52428800 bytes
# 100MB = 104857600 bytes
# 200MB = 209715200 bytes
# 500MB = 524288000 bytes
# 1GB = 1073741824 bytes

MAX_FILE_SIZE_DOCUMENTO=52428800   # 50MB padrão
MAX_FILE_SIZE_MODELO=20971520      # 20MB padrão
MAX_UPLOAD_SIZE=104857600          # 100MB padrão
```

### 2. Exemplos de Configuração

#### Para documentos pequenos (até 10MB):
```env
MAX_FILE_SIZE_DOCUMENTO=10485760   # 10MB
MAX_FILE_SIZE_MODELO=5242880       # 5MB
MAX_UPLOAD_SIZE=20971520           # 20MB
```

#### Para documentos grandes (até 200MB):
```env
MAX_FILE_SIZE_DOCUMENTO=209715200  # 200MB
MAX_FILE_SIZE_MODELO=52428800      # 50MB
MAX_UPLOAD_SIZE=314572800          # 300MB
```

#### Para documentos muito grandes (até 500MB):
```env
MAX_FILE_SIZE_DOCUMENTO=524288000  # 500MB
MAX_FILE_SIZE_MODELO=104857600     # 100MB
MAX_UPLOAD_SIZE=629145600          # 600MB
```

#### Para desabilitar limite (não recomendado):
```env
MAX_FILE_SIZE_DOCUMENTO=1073741824  # 1GB
MAX_FILE_SIZE_MODELO=524288000      # 500MB
MAX_UPLOAD_SIZE=2147483648          # 2GB
```

## 🎯 Validações Implementadas

### Backend (Python/FastAPI)

1. **Validação durante upload**: O arquivo é lido em chunks de 1MB e verificado durante o upload
2. **Validação final**: Verificação do tamanho total antes de processar
3. **Mensagens de erro claras**: Informa o tamanho máximo permitido e o tamanho do arquivo enviado

### Frontend (React)

1. **Validação antes do upload**: Verifica o tamanho antes de enviar ao servidor
2. **Feedback visual**: Mostra mensagem de erro se o arquivo for muito grande
3. **Formatação de tamanho**: Exibe tamanho do arquivo em formato legível (MB, GB)

## ⚠️ Considerações Importantes

### Performance

- **Arquivos grandes** podem levar mais tempo para processar
- **OCR em PDFs escaneados** pode ser lento para arquivos grandes
- **Extração de texto** pode consumir mais memória

### Limitações do Render (Plano Gratuito)

- **Timeout**: Requisições podem expirar após alguns minutos
- **Memória**: Limitada no plano gratuito
- **Processamento**: Pode ser mais lento para arquivos grandes

### Recomendações

1. **Para documentos pequenos** (< 10MB): Use limites menores para melhor performance
2. **Para documentos médios** (10-50MB): Limites padrão são adequados
3. **Para documentos grandes** (> 50MB): Considere aumentar limites e timeout
4. **Para documentos muito grandes** (> 200MB): Considere processar em partes ou usar plano pago

## 🔍 Como Verificar o Tamanho do Arquivo

### No Frontend

O componente `DropZone` mostra o tamanho do arquivo selecionado automaticamente.

### No Backend

O endpoint retorna informações sobre o arquivo:

```json
{
  "success": true,
  "message": "Documento processado com sucesso",
  "texto_extraido": "...",
  "filename": "documento.pdf",
  "file_size": 5242880,
  "file_size_mb": 5.0
}
```

## 🐛 Troubleshooting

### Erro: "Arquivo muito grande"

**Solução**: Aumente o limite correspondente nas variáveis de ambiente e reinicie o servidor.

### Erro: "Request timeout"

**Solução**: 
1. Aumente o `timeout_keep_alive` no `main.py`
2. Considere aumentar os limites de tamanho
3. Verifique se o arquivo não está corrompido

### Erro: "Memory error"

**Solução**:
1. Reduza os limites de tamanho
2. Processe arquivos menores
3. Considere upgrade do plano no Render

## 📊 Tabela de Conversão

| Bytes | KB | MB | GB |
|-------|----|----|----|
| 1048576 | 1024 | 1 | - |
| 10485760 | 10240 | 10 | - |
| 52428800 | 51200 | 50 | - |
| 104857600 | 102400 | 100 | - |
| 209715200 | 204800 | 200 | - |
| 524288000 | 512000 | 500 | - |
| 1073741824 | 1048576 | 1024 | 1 |

## 💡 Dicas

1. **Teste com arquivos de diferentes tamanhos** para encontrar o limite ideal
2. **Monitore o uso de memória** no Render dashboard
3. **Configure limites menores em desenvolvimento** para detectar problemas cedo
4. **Use limites maiores apenas quando necessário** para melhor performance geral

---

*Última atualização: Sistema de limites configuráveis implementado*

