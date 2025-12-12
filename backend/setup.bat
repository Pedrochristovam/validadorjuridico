@echo off
REM Script de setup para Windows

echo 🚀 Configurando Validador Juridico Backend...

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado. Instale Python 3.9+ primeiro.
    exit /b 1
)

REM Cria ambiente virtual
echo 📦 Criando ambiente virtual...
python -m venv venv

REM Ativa ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instala dependencias
echo 📥 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Cria arquivo .env se nao existir
if not exist .env (
    echo 📝 Criando arquivo .env...
    copy env.example.txt .env
    echo ⚠️  Configure sua API key no arquivo .env
)

REM Cria diretorios
echo 📁 Criando diretorios...
if not exist uploads mkdir uploads
if not exist reports mkdir reports

echo ✅ Setup concluido!
echo.
echo Para iniciar o servidor:
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Ou use:
echo   python run.py

pause


