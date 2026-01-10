# 📦 Guia de Instalação Detalhado - Prime

Este guia fornece instruções passo a passo para instalação completa do Prime.

## Pré-requisitos

- Python 3.10 ou superior
- Git instalado
- Ollama instalado e rodando
- Câmera e microfone (opcional)

## Instalação do Python

### Windows

1. Baixe Python de https://www.python.org/downloads/
2. **IMPORTANTE**: Durante a instalação, marque "Add Python to PATH"
3. Verifique a instalação:
   ```powershell
   python --version
   ```

### Linux/Mac

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Mac (com Homebrew)
brew install python3
```

## Instalação do Ollama

1. Acesse https://ollama.ai
2. Baixe e instale o Ollama
3. Inicie o Ollama
4. Baixe um modelo:
   ```bash
   ollama pull phi3
   # ou
   ollama pull mistral
   ```

## Instalação do Prime

### 1. Clone o repositório

```bash
git clone https://github.com/Usales/Prime.git
cd Prime
```

### 2. Crie ambiente virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota**: Algumas dependências são opcionais:
- `openai-whisper` - Para reconhecimento de voz (muito pesado)
- `chromadb` - Para memória semântica (muitas dependências)

### 4. Configure variáveis de ambiente

```bash
# Copie o template
cp env_template.txt .env

# Edite .env com suas configurações
```

## Verificação da Instalação

```bash
# Ative o ambiente virtual
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Verifique Python
python --version

# Verifique pacotes instalados
pip list | grep fastapi
pip list | grep ollama
```

## Executando

```bash
python main.py
```

O servidor estará disponível em `http://localhost:8000`

## Troubleshooting

### Erro: "Python não encontrado"
- Reinstale Python marcando "Add to PATH"
- Reinicie o terminal

### Erro: "pip não encontrado"
```bash
python -m ensurepip --upgrade
```

### Erro ao ativar venv (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "No space left on device"
- Libere espaço no disco
- Instale dependências pesadas separadamente quando necessário

## Próximos Passos

Após instalação bem-sucedida:
1. Configure o arquivo `.env`
2. Inicie o Ollama
3. Execute `python main.py`
4. Acesse `http://localhost:8000/status` para verificar
