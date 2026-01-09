# ⚡ Solução Rápida - Python não encontrado

## 🎯 Problema

O comando `python` está apontando para um atalho do Microsoft Store que não funciona.

## ✅ Solução Mais Rápida

### Opção 1: Instalar Python via Microsoft Store (2 minutos)

1. Abra a **Microsoft Store** (procure "Microsoft Store" no menu iniciar)
2. Procure por **"Python 3.12"** ou **"Python 3.11"**
3. Clique em **"Instalar"** (grátis)
4. Aguarde a instalação
5. **Feche e reabra o PowerShell**
6. Teste: `python --version`

### Opção 2: Usar Script Automático

Execute o script que tenta diferentes métodos:

```powershell
.\setup.ps1
```

O script tentará:
- `python`
- `py` (launcher do Windows)
- `python3`

## 🔧 Após Instalar Python

### 1. Criar Ambiente Virtual

```powershell
python -m venv venv
```

### 2. Ativar Ambiente

```powershell
.\venv\Scripts\Activate.ps1
```

**Se der erro de política:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar Dependências

```powershell
pip install -r requirements.txt
```

## 📝 Verificação

```powershell
python --version    # Deve mostrar Python 3.x.x
pip --version       # Deve mostrar pip x.x.x
```

## 🚀 Próximo Passo

Depois de instalar Python e criar o venv:

```powershell
# Ativar venv
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar Prime
python main.py
```

---

**Dica**: Se preferir instalar do site oficial (mais controle):
- https://www.python.org/downloads/
- ⚠️ **Marque "Add Python to PATH"** durante instalação
