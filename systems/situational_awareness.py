"""
Sistema de Consciência Situacional
Mantém o estado do mundo - NÃO fala, apenas observa
"""

from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass, field
import json


@dataclass
class SituationalState:
    """Estado interno do mundo percebido"""
    hora: str = ""
    luz: str = "desconhecida"  # baixa, media, alta, desconhecida
    usuario_presente: bool = False
    usuario_estado: str = "desconhecido"  # cansado, agitado, normal, desconhecido
    interacao_recente: bool = False
    ambiente: str = "desconhecido"  # silencioso, barulhento, normal
    ultima_atualizacao: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Converte estado para dicionário"""
        return {
            "hora": self.hora,
            "luz": self.luz,
            "usuario_presente": self.usuario_presente,
            "usuario_estado": self.usuario_estado,
            "interacao_recente": self.interacao_recente,
            "ambiente": self.ambiente,
            "ultima_atualizacao": self.ultima_atualizacao.isoformat()
        }
    
    def to_json(self) -> str:
        """Converte estado para JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class SituationalAwareness:
    """
    Sistema que mantém consciência do ambiente
    Atualiza estado a cada poucos segundos
    """
    
    def __init__(self):
        self.state = SituationalState()
        self._update_time()
    
    def _update_time(self):
        """Atualiza hora atual"""
        now = datetime.now()
        self.state.hora = now.strftime("%H:%M")
        self.state.ultima_atualizacao = now
    
    def update_presence(self, presente: bool):
        """Atualiza detecção de presença humana"""
        self.state.usuario_presente = presente
        self._update_time()
    
    def update_user_state(self, estado: str):
        """Atualiza estado do usuário (cansado, agitado, normal)"""
        if estado in ["cansado", "agitado", "normal", "desconhecido"]:
            self.state.usuario_estado = estado
            self._update_time()
    
    def update_light(self, nivel: str):
        """Atualiza nível de luz (baixa, media, alta)"""
        if nivel in ["baixa", "media", "alta", "desconhecida"]:
            self.state.luz = nivel
            self._update_time()
    
    def update_environment(self, ambiente: str):
        """Atualiza ambiente (silencioso, barulhento, normal)"""
        if ambiente in ["silencioso", "barulhento", "normal", "desconhecido"]:
            self.state.ambiente = ambiente
            self._update_time()
    
    def mark_interaction(self, interagiu: bool = True):
        """Marca se houve interação recente"""
        self.state.interacao_recente = interagiu
        self._update_time()
    
    def tick(self):
        """Atualização periódica (chamada a cada ciclo)"""
        self._update_time()
        # Reseta interação recente após um tempo
        # (será implementado com timer depois)
    
    def get_state(self) -> SituationalState:
        """Retorna estado atual"""
        return self.state
    
    def get_state_dict(self) -> Dict:
        """Retorna estado como dicionário"""
        return self.state.to_dict()
