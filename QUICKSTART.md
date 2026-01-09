# 🚀 Quick Start - Prime

Guia rápido para começar a usar o Prime.

## 1. Instalação Rápida

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## 2. Configurar Ollama

```bash
# Instalar Ollama de https://ollama.ai
# Depois baixar modelo:
ollama pull phi3
# ou
ollama pull mistral
```

## 3. Executar

### Opção 1: Com FastAPI (recomendado)
```bash
python main.py
```

Acesse `http://localhost:8000/status` para ver o status.

### Opção 2: Standalone (sem API)
```bash
python run.py
```

## 4. Testar Sistemas

```bash
python examples/exemplo_uso.py
```

## 5. Configurar Personalidade

Edite `.env` (crie se não existir):

```env
PERSONALITY_AFETUOSA=0.6
PERSONALITY_OBSERVADORA=0.8
PERSONALITY_IRONICA=0.4
PERSONALITY_RESERVADA=0.3
PERSONALITY_CURIOSA=0.7
```

## 6. Desabilitar Câmera (se não tiver)

No `.env`:
```env
ENABLE_CAMERA=false
```

## 📝 Notas

- O Prime funciona mesmo sem câmera/microfone
- O sistema sensorial está em modo simulado por padrão
- A memória é armazenada em `./data/prime.db`
- Logs ficam no console (configure em `.env`)

## 🐛 Problemas Comuns

### Ollama não encontrado
- Certifique-se que Ollama está rodando: `ollama serve`
- Verifique a URL em `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

### Erro de importação
- Certifique-se que está no diretório `Prime`
- Ative o ambiente virtual
- Reinstale dependências: `pip install -r requirements.txt`

### TTS não funciona
- No Windows, geralmente funciona automaticamente
- No Linux, pode precisar: `sudo apt-get install espeak`

## 🎯 Próximos Passos

1. Ajuste a personalidade no `.env`
2. Monitore o status via API: `GET /status`
3. Registre interações: `POST /interaction?tipo=positiva`
4. Veja exemplos em `examples/exemplo_uso.py`

---

**Lembre-se**: O Prime é um agente "vivo", não um assistente. Ele decide quando falar ou calar!
