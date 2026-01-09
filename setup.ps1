# Script de Setup do Prime
# Tenta diferentes métodos para criar o ambiente virtual

Write-Host "=== Setup do Prime ===" -ForegroundColor Cyan
Write-Host ""

# Método 1: Tentar com python
Write-Host "Tentando método 1: python..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -notmatch "Microsoft Store" -and $pythonVersion -notmatch "não foi encontrado") {
        Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Ambiente virtual criado com sucesso!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Próximos passos:" -ForegroundColor Cyan
            Write-Host "1. Ativar: .\venv\Scripts\Activate.ps1" -ForegroundColor White
            Write-Host "2. Instalar: pip install -r requirements.txt" -ForegroundColor White
            exit 0
        }
    }
}
Write-Host "✗ python não funcionou" -ForegroundColor Red

# Método 2: Tentar com py launcher
Write-Host ""
Write-Host "Tentando método 2: py launcher..." -ForegroundColor Yellow
$pyCmd = Get-Command py -ErrorAction SilentlyContinue
if ($pyCmd) {
    $pyVersion = py --version 2>&1
    Write-Host "✓ py launcher encontrado: $pyVersion" -ForegroundColor Green
    py -3 -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Ambiente virtual criado com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Próximos passos:" -ForegroundColor Cyan
        Write-Host "1. Ativar: .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "2. Instalar: pip install -r requirements.txt" -ForegroundColor White
        exit 0
    }
} else {
    Write-Host "✗ py launcher não encontrado" -ForegroundColor Red
}

# Método 3: Tentar python3
Write-Host ""
Write-Host "Tentando método 3: python3..." -ForegroundColor Yellow
$python3Cmd = Get-Command python3 -ErrorAction SilentlyContinue
if ($python3Cmd) {
    $python3Version = python3 --version 2>&1
    Write-Host "✓ python3 encontrado: $python3Version" -ForegroundColor Green
    python3 -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Ambiente virtual criado com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Próximos passos:" -ForegroundColor Cyan
        Write-Host "1. Ativar: .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "2. Instalar: pip install -r requirements.txt" -ForegroundColor White
        exit 0
    }
} else {
    Write-Host "✗ python3 não encontrado" -ForegroundColor Red
}

# Se chegou aqui, nenhum método funcionou
Write-Host ""
Write-Host "❌ Nenhum método funcionou!" -ForegroundColor Red
Write-Host ""
Write-Host "Python não está instalado corretamente." -ForegroundColor Yellow
Write-Host ""
Write-Host "Soluções:" -ForegroundColor Cyan
Write-Host "1. Instale Python de: https://www.python.org/downloads/" -ForegroundColor White
Write-Host "   ⚠️ IMPORTANTE: Marque 'Add Python to PATH' durante instalação" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Ou instale via Microsoft Store:" -ForegroundColor White
Write-Host "   - Abra Microsoft Store" -ForegroundColor White
Write-Host "   - Procure 'Python 3.12'" -ForegroundColor White
Write-Host "   - Instale e reinicie o PowerShell" -ForegroundColor White
Write-Host ""
Write-Host "3. Veja mais detalhes em: INSTALACAO_PYTHON.md" -ForegroundColor White
Write-Host ""

exit 1
