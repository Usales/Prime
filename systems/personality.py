"""
Sistema de Personalidade
Traços nucleares que nunca mudam totalmente
Filtram decisões e limitam o LLM
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class PersonalityTraits:
    """Traços de personalidade fixos (nunca mudam totalmente)"""
    afetuosa: float = 0.6  # 0.0 a 1.0
    observadora: float = 0.8
    ironica: float = 0.4
    reservada: float = 0.3
    curiosa: float = 0.7
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "afetuosa": self.afetuosa,
            "observadora": self.observadora,
            "ironica": self.ironica,
            "reservada": self.reservada,
            "curiosa": self.curiosa
        }


class PersonalitySystem:
    """
    Sistema de personalidade
    Define identidade e limita comportamento
    """
    
    def __init__(self, traits: PersonalityTraits = None):
        if traits is None:
            self.traits = PersonalityTraits()
        else:
            self.traits = traits
    
    def get_traits(self) -> PersonalityTraits:
        """Retorna traços de personalidade"""
        return self.traits
    
    def get_traits_dict(self) -> Dict:
        """Retorna traços como dicionário"""
        return self.traits.to_dict()
    
    def filter_decision(self, decisao: str, contexto: Dict) -> bool:
        """
        Filtra decisões baseado em personalidade
        Retorna True se a decisão é compatível com a personalidade
        """
        # Exemplo: se é muito reservada, evita falar demais
        if decisao == "falar_muito" and self.traits.reservada > 0.5:
            return False
        
        # Se é observadora, prefere observar antes de agir
        if decisao == "agir_rapido" and self.traits.observadora > 0.7:
            return False
        
        return True
    
    def get_llm_constraints(self) -> str:
        """
        Retorna constraints para o LLM baseado na personalidade
        Isso será usado no prompt do sistema
        """
        constraints = []
        
        if self.traits.reservada > 0.5:
            constraints.append("Você fala pouco. Prefere silêncio.")
        
        if self.traits.afetuosa > 0.6:
            constraints.append("Você é afetuosa, mas não exagerada.")
        
        if self.traits.ironica > 0.4:
            constraints.append("Você tem um toque de ironia sutil.")
        
        if self.traits.observadora > 0.7:
            constraints.append("Você observa antes de falar.")
        
        if self.traits.curiosa > 0.6:
            constraints.append("Você é curiosa, mas não invasiva.")
        
        return " ".join(constraints) if constraints else ""
