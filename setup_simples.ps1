# Script Simples de Setup do Prime

Write-Host "=== Setup do Prime ===" -ForegroundColor Cyan
Write-Host ""

# Verifica se Python está instalado
Write-Host "Verificando Python..." -ForegroundColor Yellow

# Tenta python
$pythonOk = $false
try {
    $result = python --version 2>&1
    if ($result -notmatch "Microsoft Store" -and $result -notmatch "não foi encontrado") {
        Write-Host "Python encontrado: $result" -ForegroundColor Green
        python -m venv venv
        if ($?) {
            $pythonOk = $true
        }
    }
} catch {
    # Ignora
}

# Se não funcionou, tenta py
if (-not $pythonOk) {
    try {
        $result = py --version 2>&1
        if ($?) {
            Write-Host "py launcher encontrado: $result" -ForegroundColor Green
            py -3 -m venv venv
            if ($?) {
                $pythonOk = $true
            }
        }
    } catch {
        # Ignora
    }
}

# Resultado
if ($pythonOk) {
    Write-Host ""
    Write-Host "SUCESSO! Ambiente virtual criado." -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos passos:" -ForegroundColor Cyan
    Write-Host "1. .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "2. pip install -r requirements.txt" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instale Python:" -ForegroundColor Yellow
    Write-Host "1. Microsoft Store: Procure 'Python 3.12'" -ForegroundColor White
    Write-Host "2. Ou: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "   (Marque 'Add Python to PATH')" -ForegroundColor Yellow
}
