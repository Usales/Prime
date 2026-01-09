"""
Sistema Emocional (Homeostase)
Emoções são variáveis internas que buscam equilíbrio
NÃO são respostas, são estados que mudam com o tempo
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict
import random


@dataclass
class EmotionalState:
    """Estado emocional interno"""
    energia: float = 0.5  # 0.0 a 1.0
    curiosidade: float = 0.5
    necessidade_social: float = 0.5
    irritacao: float = 0.0
    apego: float = 0.3
    ultima_atualizacao: datetime = field(default_factory=datetime.now)
    
    def clamp(self):
        """Garante que valores fiquem entre 0.0 e 1.0"""
        self.energia = max(0.0, min(1.0, self.energia))
        self.curiosidade = max(0.0, min(1.0, self.curiosidade))
        self.necessidade_social = max(0.0, min(1.0, self.necessidade_social))
        self.irritacao = max(0.0, min(1.0, self.irritacao))
        self.apego = max(0.0, min(1.0, self.apego))
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "energia": round(self.energia, 3),
            "curiosidade": round(self.curiosidade, 3),
            "necessidade_social": round(self.necessidade_social, 3),
            "irritacao": round(self.irritacao, 3),
            "apego": round(self.apego, 3),
            "ultima_atualizacao": self.ultima_atualizacao.isoformat()
        }


class EmotionalSystem:
    """
    Sistema emocional com homeostase
    Valores mudam com o tempo e eventos
    """
    
    def __init__(self):
        self.state = EmotionalState()
        self._decay_rate = 0.001  # Taxa de decaimento por tick
        self._social_decay_rate = 0.002  # Necessidade social aumenta mais rápido
    
    def tick(self, situacional_state: Dict):
        """
        Atualização periódica baseada no estado situacional
        Aplica homeostase e mudanças graduais
        """
        # Decaimento natural (tendência ao equilíbrio)
        self._apply_decay()
        
        # Mudanças baseadas em situação
        self._react_to_situation(situacional_state)
        
        # Garante limites
        self.state.clamp()
        self.state.ultima_atualizacao = datetime.now()
    
    def _apply_decay(self):
        """Aplica decaimento natural (homeostase)"""
        # Energia tende a aumentar lentamente
        if self.state.energia < 0.5:
            self.state.energia += self._decay_rate * 0.5
        else:
            self.state.energia -= self._decay_rate * 0.3
        
        # Curiosidade tende ao meio
        if self.state.curiosidade > 0.5:
            self.state.curiosidade -= self._decay_rate
        else:
            self.state.curiosidade += self._decay_rate * 0.5
        
        # Irritação sempre decai
        if self.state.irritacao > 0:
            self.state.irritacao -= self._decay_rate * 2
        
        # Apego decai muito lentamente
        if self.state.apego > 0.2:
            self.state.apego -= self._decay_rate * 0.1
    
    def _react_to_situation(self, situacional: Dict):
        """Reage ao estado situacional"""
        # Longo silêncio → aumenta necessidade social
        if not situacional.get("interacao_recente", False):
            tempo_sem_interacao = self._calculate_silence_time()
            if tempo_sem_interacao > 300:  # 5 minutos
                self.state.necessidade_social += self._social_decay_rate * 3
            elif tempo_sem_interacao > 60:  # 1 minuto
                self.state.necessidade_social += self._social_decay_rate
        
        # Usuário presente mas sem interação → aumenta necessidade social
        if situacional.get("usuario_presente", False) and not situacional.get("interacao_recente", False):
            self.state.necessidade_social += self._social_decay_rate * 2
        
        # Usuário cansado → reduz energia (empatia)
        if situacional.get("usuario_estado") == "cansado":
            self.state.energia -= self._decay_rate * 0.5
        
        # Ambiente barulhento → aumenta irritação
        if situacional.get("ambiente") == "barulhento":
            self.state.irritacao += self._decay_rate * 1.5
    
    def _calculate_silence_time(self) -> float:
        """Calcula tempo desde última interação (simplificado)"""
        # Por enquanto retorna um valor simulado
        # Depois será baseado em memória
        return 120.0  # 2 minutos simulado
    
    def on_interaction(self, tipo: str = "normal"):
        """
        Reage a uma interação do usuário
        tipo: "normal", "positiva", "negativa", "ignorada"
        """
        if tipo == "positiva":
            self.state.apego += 0.1
            self.state.energia += 0.05
            self.state.necessidade_social -= 0.2
        elif tipo == "negativa":
            self.state.irritacao += 0.1
            self.state.energia -= 0.05
        elif tipo == "ignorada":
            self.state.irritacao += 0.05
            self.state.necessidade_social += 0.1
        else:  # normal
            self.state.necessidade_social -= 0.1
            self.state.curiosidade += 0.02
        
        self.state.clamp()
    
    def on_long_silence(self, minutos: float):
        """Reage a longo silêncio"""
        if minutos > 30:
            self.state.necessidade_social += 0.3
            self.state.curiosidade += 0.1
        elif minutos > 10:
            self.state.necessidade_social += 0.1
    
    def on_energy_depletion(self):
        """Reage quando energia está baixa"""
        self.state.energia -= 0.1
    
    def get_state(self) -> EmotionalState:
        """Retorna estado emocional atual"""
        return self.state
    
    def get_state_dict(self) -> Dict:
        """Retorna estado como dicionário"""
        return self.state.to_dict()
