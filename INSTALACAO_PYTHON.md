# 🐍 Instalação do Python - Windows

## Problema Identificado

O comando `python` está apontando para um atalho do Microsoft Store que não funciona corretamente.

## ✅ Solução: Instalar Python Corretamente

### Opção 1: Instalar do Site Oficial (Recomendado)

1. **Baixar Python:**
   - Acesse: https://www.python.org/downloads/
   - Baixe a versão mais recente (Python 3.11 ou 3.12)
   - Escolha o instalador Windows (64-bit)

2. **Durante a Instalação:**
   - ✅ **IMPORTANTE**: Marque a opção **"Add Python to PATH"**
   - Escolha "Install Now" ou "Customize installation"
   - Se escolher "Customize", certifique-se de marcar "Add Python to PATH"

3. **Verificar Instalação:**
   ```powershell
   python --version
   ```
   Deve mostrar algo como: `Python 3.12.x`

4. **Verificar pip:**
   ```powershell
   pip --version
   ```

### Opção 2: Usar Microsoft Store (Mais Simples)

1. Abra a Microsoft Store
2. Procure por "Python 3.12" ou "Python 3.11"
3. Clique em "Instalar"
4. Após instalar, feche e reabra o PowerShell
5. Teste: `python --version`

### Opção 3: Usar py Launcher (Já Instalado no Windows)

Se você já tem Python instalado mas não está no PATH:

```powershell
# Verificar versões disponíveis
py -0

# Criar venv usando py launcher
py -3.12 -m venv venv

# Ou usar a versão mais recente
py -3 -m venv venv
```

## 🔧 Após Instalar Python

### 1. Criar Ambiente Virtual

```powershell
cd C:\Users\GABRIEL-SUP\Desktop\Projetos\Prime
python -m venv venv
```

### 2. Ativar Ambiente Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

**Se der erro de política de execução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 4. Verificar Instalação

```powershell
python --version
pip list
```

## 🐛 Problemas Comuns

### "python não é reconhecido"

**Solução:**
1. Reinstale Python marcando "Add to PATH"
2. Ou adicione manualmente ao PATH:
   - Procure "Variáveis de Ambiente" no Windows
   - Adicione `C:\Python3xx` e `C:\Python3xx\Scripts` ao PATH
   - Reinicie o PowerShell

### "pip não é reconhecido"

**Solução:**
```powershell
python -m ensurepip --upgrade
```

### Erro ao ativar venv

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## ✅ Verificação Final

Execute estes comandos para verificar:

```powershell
python --version
pip --version
python -m venv --help
```

Todos devem funcionar sem erros.

## 📝 Próximos Passos

Após instalar Python corretamente:

1. ✅ Criar venv: `python -m venv venv`
2. ✅ Ativar: `.\venv\Scripts\Activate.ps1`
3. ✅ Instalar: `pip install -r requirements.txt`
4. ✅ Configurar: Copie `env_template.txt` para `.env`
5. ✅ Executar: `python main.py`

---

**Dica**: Se continuar com problemas, use o **py launcher** que vem com Windows:
```powershell
py -3 -m venv venv
```
