"""
Prime - Sistema de Agente Vivo
Módulo de sistemas independentes

O Prime é composto por 7 sistemas independentes:
1. Sistema Sensorial - Percepção (visão e audição)
2. Sistema de Consciência Situacional - Estado do mundo
3. Sistema Emocional - Homeostase (emoções como variáveis internas)
4. Sistema de Personalidade - Traços nucleares fixos
5. Sistema de Memória Viva - Memórias com peso emocional
6. Sistema de Decisão Autônoma - Lógica + emoção + personalidade
7. Sistema de Expressão - LLM + TTS (apenas verbaliza)
"""

__version__ = "0.1.0"

# Importações dos sistemas principais
from .sensory import SensorySystem
from .situational_awareness import SituationalAwareness
from .emotional_system import EmotionalSystem
from .personality import PersonalitySystem
from .memory import MemorySystem
from .decision import DecisionSystem
from .expression import ExpressionSystem

__all__ = [
    "SensorySystem",
    "SituationalAwareness",
    "EmotionalSystem",
    "PersonalitySystem",
    "MemorySystem",
    "DecisionSystem",
    "ExpressionSystem",
]
