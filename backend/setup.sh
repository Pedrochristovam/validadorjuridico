#!/bin/bash
# Script de setup para Linux/macOS

echo "🚀 Configurando Validador Jurídico Backend..."

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.9+ primeiro."
    exit 1
fi

# Cria ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp env.example.txt .env
    echo "⚠️  Configure sua API key no arquivo .env"
fi

# Cria diretórios
echo "📁 Criando diretórios..."
mkdir -p uploads reports

echo "✅ Setup concluído!"
echo ""
echo "Para iniciar o servidor:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Ou use:"
echo "  python run.py"


