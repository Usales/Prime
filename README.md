# 🧬 Prime - Agente Vivo

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/Usales/Prime)

Um agente "vivo" que **NÃO é um LLM**. O LLM é apenas o aparelho fonador e linguístico.

## 🧠 Arquitetura

O Prime é composto por **7 sistemas independentes** que trabalham juntos:

1. **Sistema Sensorial** - Percepção (visão e audição)
2. **Sistema de Consciência Situacional** - Estado do mundo
3. **Sistema Emocional** - Homeostase (emoções como variáveis internas)
4. **Sistema de Personalidade** - Traços nucleares fixos
5. **Sistema de Memória Viva** - Memórias com peso emocional
6. **Sistema de Decisão Autônoma** - Lógica + emoção + personalidade
7. **Sistema de Expressão** - LLM + TTS (apenas verbaliza)

## 🎯 Princípios Fundamentais

- **Percepção contínua** - Sempre observando, mesmo em silêncio
- **Estados internos mutáveis** - Emoções mudam com o tempo
- **Memória afetiva** - Lembra com peso emocional
- **Iniciativa própria** - Decide quando falar ou calar
- **Imperfeição controlada** - Erros propositais = realismo

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Ollama instalado e rodando (com modelo phi3 ou mistral)
- Câmera e microfone (opcional, pode funcionar sem)

### Passos

1. Clone ou navegue até o diretório:
```bash
cd Prime
```

2. Crie ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale dependências:
```bash
pip install -r requirements.txt
```

4. Configure variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Instale Ollama e baixe modelo:
```bash
# Instale Ollama de https://ollama.ai
ollama pull phi3
```

## 🏃 Executando

### Modo Desenvolvimento

```bash
python main.py
```

O servidor FastAPI estará disponível em `http://localhost:8000`

### Endpoints

- `GET /` - Informações básicas
- `GET /status` - Status completo de todos os sistemas
- `GET /health` - Health check
- `POST /interaction?tipo=normal` - Registra interação do usuário

### Modo Standalone (sem FastAPI)

```python
from prime_core import PrimeCore
import asyncio

async def main():
    prime = PrimeCore()
    await prime.run(tick_interval=5.0)

asyncio.run(main())
```

## 📁 Estrutura do Projeto

```
Prime/
├── systems/              # 7 sistemas independentes
│   ├── situational_awareness.py
│   ├── emotional_system.py
│   ├── personality.py
│   ├── memory.py
│   ├── sensory.py
│   ├── decision.py
│   └── expression.py
├── config/
│   └── settings.py       # Configurações
├── data/                 # Banco de dados e dados
├── logs/                 # Logs
├── prime_core.py         # Orquestrador principal
├── main.py               # FastAPI + entrada principal
├── requirements.txt
└── README.md
```

## 🔧 Configuração

Edite `.env` para personalizar:

- **Personalidade**: Ajuste traços (0.0 a 1.0)
- **Ollama**: URL e modelo
- **Sensorial**: Habilitar/desabilitar câmera e microfone
- **Database**: Caminho do banco de dados

## 🧪 Como Funciona

1. **Tick a cada 5 segundos** (configurável)
2. **Sistema Sensorial** detecta presença (se habilitado)
3. **Consciência Situacional** atualiza estado do mundo
4. **Sistema Emocional** aplica homeostase
5. **Sistema de Decisão** avalia todos os fatores
6. **Se decidir falar**: LLM gera resposta → TTS fala
7. **Memória** registra evento com peso emocional

## 🎭 Personalidade

A personalidade é definida por traços fixos que filtram decisões:

- **Afetuosa** (0.6) - Carinhosa, mas não exagerada
- **Observadora** (0.8) - Observa antes de falar
- **Irônica** (0.4) - Toque sutil de ironia
- **Reservada** (0.3) - Fala pouco, prefere silêncio
- **Curiosa** (0.7) - Curiosa, mas não invasiva

## 🧠 Memória

Três níveis de memória:

- **Curto prazo**: Últimas 20 interações (em memória)
- **Médio prazo**: Padrões e hábitos (SQLite)
- **Longo prazo**: Momentos marcantes com alto peso emocional

## ⚠️ Importante

- O LLM **NUNCA decide** emoções ou iniciativa
- O LLM apenas **verbaliza** decisões já tomadas
- Às vezes o Prime **não faz nada** - isso é válido!
- Imperfeição é proposital - erros = realismo

## 🛠️ Stack

- **Python 3.10+**
- **FastAPI** - API REST
- **OpenCV/MediaPipe** - Visão
- **Whisper** - Reconhecimento de voz (futuro)
- **Ollama** - LLM local
- **pyttsx3** - TTS
- **SQLite** - Banco de dados
- **ChromaDB** - Memória semântica (futuro)

## 📝 Licença

Projeto pessoal - uso livre

## 📚 Documentação

- [INSTALL.md](INSTALL.md) - Guia completo de instalação
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guia para contribuidores
- [CHANGELOG.md](CHANGELOG.md) - Histórico de mudanças
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detalhes da arquitetura
- [STATUS.md](STATUS.md) - Status do projeto

## 🤝 Contribuindo

Este é um projeto experimental. Sugestões são bem-vindas!

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes sobre como contribuir.

---

**Lembre-se**: Um agente "vivo" não é um LLM. O LLM é apenas a voz.
