# Fluxo do Sistema - Validador Jurídico

## Como Funciona:

### 1. **Cadastro de Modelo** (Página "Modelos")
- Usuário faz upload de um arquivo Word (.docx) que contém o modelo/template a ser seguido
- Sistema extrai o texto do arquivo Word
- Salva o modelo com:
  - Nome do modelo
  - Arquivo original
  - Texto extraído do modelo

### 2. **Validação de Documento** (Página "Home")
- Usuário seleciona um modelo cadastrado (opcional, pode usar o padrão)
- Usuário faz upload do documento que deseja validar (PDF ou DOCX)
- Sistema:
  1. Extrai o texto do documento enviado
  2. Se um modelo foi selecionado, compara com o texto do modelo
  3. Valida conforme as regras específicas (últimos 5 anos, valores >= 2.500.000, etc.)
  4. Retorna resultados:
     - ✅ Requisitos corretos
     - ❌ Requisitos faltando
     - ⚠️ Requisitos duvidosos
     - Evidências encontradas

### 3. **Regras de Validação**
O sistema valida automaticamente:
- **Lote 1 (Tributário e Previdenciário):**
  - 5 defesas administrativas >= R$ 2.500.000 nos últimos 5 anos com resultado exitoso
  - 5 processos judiciais >= R$ 2.500.000 nos últimos 5 anos com resultado exitoso
  - Histórico profissional com lista de processos
  - Capacidade contábil/fiscal/financeira

- **Lote 2 (PIS e COFINS):**
  - 5 defesas administrativas em securitização >= R$ 2.500.000
  - 5 processos judiciais em securitização >= R$ 2.500.000
  - Histórico profissional em securitização
  - Capacidade contábil para securitização e debêntures

- **Comprovações obrigatórias:**
  - Sentenças favoráveis
  - Certidões de trânsito em julgado





