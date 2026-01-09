# 🏗️ Arquitetura do Prime

## Visão Geral

O Prime é um agente "vivo" composto por **7 sistemas independentes** que trabalham em conjunto para criar uma presença doméstica autônoma.

## 🧠 Princípio Fundamental

> **Um agente "vivo" NÃO é um LLM.**
> 
> O LLM é apenas o aparelho fonador e linguístico.
> 
> O "vivo" nasce de:
> - Percepção contínua
> - Estados internos mutáveis
> - Memória afetiva
> - Iniciativa própria
> - Imperfeição controlada

## 📊 Diagrama de Sistemas

```
┌─────────────────────────────────────────────────────────┐
│                    PRIME CORE                            │
│              (Orquestrador Principal)                     │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Sensorial   │  │ Situacional  │  │  Emocional   │
│  (Visão/Áudio)│  │  (Estado)    │  │ (Homeostase) │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Memória     │  │ Personalidade│  │  Decisão     │
│  (SQLite)    │  │  (Traços)    │  │ (Autônoma)   │
└──────────────┘  └──────────────┘  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │  Expressão   │
                  │ (LLM + TTS)  │
                  └──────────────┘
```

## 🔄 Fluxo de Execução

### 1. Ciclo Principal (Tick)

```
A cada 5 segundos:
  1. Sistema Sensorial → Detecta presença/ambiente
  2. Consciência Situacional → Atualiza estado do mundo
  3. Sistema Emocional → Aplica homeostase
  4. Sistema de Decisão → Avalia todos os fatores
  5. Se decidir falar → Sistema de Expressão gera resposta
  6. Memória → Armazena evento com peso emocional
```

### 2. Pipeline Sensorial

```
Sensor de Movimento
    ↓
Ativa Câmera
    ↓
Detecta Forma Humana
    ↓
Classifica Contexto
    ↓
Desliga Câmera
    ↓
Atualiza Estado Situacional
```

### 3. Sistema de Decisão

```
Inputs:
  - Estado Emocional (5 variáveis)
  - Estado Situacional (6 variáveis)
  - Personalidade (5 traços)
  - Memória Recente (últimas 5 interações)

Processamento:
  - Calcula score para cada ação
  - Aplica imprevisibilidade controlada
  - Filtra por personalidade

Output:
  - Decisão: FALAR | SILENCIO | OBSERVAR | MUDAR_HUMOR | NADA
  - Intensidade: 0.0 a 1.0
  - Motivo: string descritiva
```

## 📦 Estrutura de Dados

### Estado Situacional

```python
{
  "hora": "19:42",
  "luz": "baixa",
  "usuario_presente": true,
  "usuario_estado": "cansado",
  "interacao_recente": false,
  "ambiente": "silencioso"
}
```

### Estado Emocional

```python
{
  "energia": 0.32,
  "curiosidade": 0.67,
  "necessidade_social": 0.81,
  "irritacao": 0.12,
  "apego": 0.45
}
```

### Personalidade

```python
{
  "afetuosa": 0.6,
  "observadora": 0.8,
  "ironica": 0.4,
  "reservada": 0.3,
  "curiosa": 0.7
}
```

## 🔌 Interfaces entre Sistemas

### Sensorial → Situacional
- Presença detectada → `update_presence()`
- Estado do usuário → `update_user_state()`
- Nível de luz → `update_light()`

### Situacional → Emocional
- Estado situacional → `tick(situacional_state)`
- Aplica homeostase baseado em situação

### Emocional → Decisão
- Estado emocional → `decide(emocional, ...)`
- Usado para calcular scores

### Decisão → Expressão
- Decisão tomada → `generate_response(decisao, ...)`
- LLM apenas verbaliza, não decide

### Memória → Todos
- Eventos armazenados → Influencia decisões futuras
- Padrões identificados → Ajusta comportamento

## 🛡️ Resiliência

Cada sistema é **independente**:

- Se um sistema falhar, os outros continuam
- Não há dependências críticas entre sistemas
- Cada sistema pode ser testado isoladamente
- Fácil adicionar novos sistemas

## 🎯 Princípios de Design

1. **Separação de Responsabilidades**
   - Cada sistema tem uma função única
   - Não há acoplamento forte

2. **Falha Isolada**
   - Erro em um sistema não derruba outros
   - Graceful degradation

3. **Extensibilidade**
   - Fácil adicionar novos sistemas
   - Interfaces bem definidas

4. **Testabilidade**
   - Sistemas podem ser testados isoladamente
   - Mocks fáceis de criar

## 📈 Escalabilidade

- **Horizontal**: Adicionar mais sistemas
- **Vertical**: Melhorar cada sistema individualmente
- **Distribuída**: Sistemas podem rodar em processos separados (futuro)

## 🔮 Futuras Melhorias

- [ ] ChromaDB para memória semântica
- [ ] MQTT para eventos externos
- [ ] Detecção real de presença (MediaPipe)
- [ ] Whisper para reconhecimento de voz
- [ ] Sistema de seeds diárias mais sofisticado
- [ ] Interface visual (opcional)

---

**Arquitetura v0.1.0** - Janeiro 2026
