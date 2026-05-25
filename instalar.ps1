# Verificar se a versão do Python é menor que 3.11
$pythonVersion = (python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

if ([version]$pythonVersion -lt [version]"3.11") {
    Write-Host "⚠️ Python está desatualizado (Versão: $pythonVersion). Atualizando via Winget..." -ForegroundColor Yellow
    
    # Instala o Python 3.12 automaticamente usando o gerenciador de pacotes do Windows
    winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
    
    Write-Host "✅ Python instalado! Por favor, FECHE e ABRA o terminal novamente para aplicar as mudanças." -ForegroundColor Green
    Exit
}

Write-Host "🚀 Python atualizado ($pythonVersion). Criando ambiente virtual..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Ativa o ambiente e instala as dependências
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "🎉 Tudo pronto e pronto para uso!" -ForegroundColor Green
