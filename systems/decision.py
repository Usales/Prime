"""
Sistema de Decisão Autônoma
Coração do agente vivo
Decide: falar, ficar em silêncio, observar, mudar de humor
Decisão NÃO é LLM - é lógica + emoção + personalidade
"""

from typing import Dict, Optional, List
from enum import Enum
import random


class DecisionType(Enum):
    """Tipos de decisão possíveis"""
    FALAR = "falar"
    SILENCIO = "silenciar"
    OBSERVAR = "observar"
    MUDAR_HUMOR = "mudar_humor"
    NADA = "nada"


class Decision:
    """Representa uma decisão tomada"""
    def __init__(self, tipo: DecisionType, intensidade: float = 0.5, 
                 motivo: str = "", contexto: Dict = None):
        self.tipo = tipo
        self.intensidade = intensidade  # 0.0 a 1.0
        self.motivo = motivo
        self.contexto = contexto or {}
        self.timestamp = None
    
    def to_dict(self) -> Dict:
        """Converte decisão para dicionário"""
        return {
            "tipo": self.tipo.value,
            "intensidade": self.intensidade,
            "motivo": self.motivo,
            "contexto": self.contexto
        }


class DecisionSystem:
    """
    Sistema de decisão autônoma
    Combina: emoção + situação + personalidade + memória
    """
    
    def __init__(self, seed_diaria: Optional[int] = None):
        # Seed diária para imprevisibilidade controlada
        if seed_diaria is None:
            from datetime import datetime
            seed_diaria = int(datetime.now().strftime("%Y%m%d"))
        random.seed(seed_diaria)
        self._random_factor = random.random()
    
    def decide(self, 
               emocional: Dict,
               situacional: Dict,
               personalidade: Dict,
               memoria_recente: List = None) -> Decision:
        """
        Toma uma decisão baseada em todos os sistemas
        """
        memoria_recente = memoria_recente or []
        
        # Calcula scores para cada tipo de ação
        scores = {
            DecisionType.FALAR: self._score_falar(emocional, situacional, personalidade),
            DecisionType.SILENCIO: self._score_silenciar(emocional, situacional, personalidade),
            DecisionType.OBSERVAR: self._score_observar(emocional, situacional, personalidade),
            DecisionType.MUDAR_HUMOR: self._score_mudar_humor(emocional),
            DecisionType.NADA: self._score_nada(emocional, situacional)
        }
        
        # Aplica imprevisibilidade controlada
        scores = self._apply_randomness(scores)
        
        # Seleciona decisão com maior score
        melhor_decisao = max(scores.items(), key=lambda x: x[1])
        tipo, score = melhor_decisao
        
        # Se score muito baixo, escolhe NADA
        if score < 0.3:
            tipo = DecisionType.NADA
            score = 0.3
        
        # Gera motivo
        motivo = self._generate_motivo(tipo, emocional, situacional)
        
        return Decision(
            tipo=tipo,
            intensidade=score,
            motivo=motivo,
            contexto={
                "scores": {k.value: v for k, v in scores.items()},
                "emocional": emocional,
                "situacional": situacional
            }
        )
    
    def _score_falar(self, emocional: Dict, situacional: Dict, personalidade: Dict) -> float:
        """Calcula score para falar"""
        score = 0.0
        
        # Necessidade social alta → quer falar
        if emocional.get("necessidade_social", 0) > 0.7:
            score += 0.4
        
        # Usuário presente e sem interação recente
        if situacional.get("usuario_presente") and not situacional.get("interacao_recente"):
            score += 0.3
        
        # Curiosidade alta
        if emocional.get("curiosidade", 0) > 0.6:
            score += 0.2
        
        # Energia suficiente
        if emocional.get("energia", 0) > 0.3:
            score += 0.1
        else:
            score -= 0.2  # Sem energia, não quer falar
        
        # Personalidade reservada reduz score
        if personalidade.get("reservada", 0) > 0.5:
            score *= 0.6
        
        # Irritação alta reduz vontade de falar
        if emocional.get("irritacao", 0) > 0.5:
            score *= 0.5
        
        return min(1.0, max(0.0, score))
    
    def _score_silenciar(self, emocional: Dict, situacional: Dict, personalidade: Dict) -> float:
        """Calcula score para ficar em silêncio"""
        score = 0.0
        
        # Personalidade reservada prefere silêncio
        if personalidade.get("reservada", 0) > 0.5:
            score += 0.4
        
        # Energia baixa → prefere silêncio
        if emocional.get("energia", 0) < 0.3:
            score += 0.3
        
        # Interação recente → pode descansar
        if situacional.get("interacao_recente"):
            score += 0.2
        
        # Usuário ausente → silêncio natural
        if not situacional.get("usuario_presente"):
            score += 0.3
        
        return min(1.0, max(0.0, score))
    
    def _score_observar(self, emocional: Dict, situacional: Dict, personalidade: Dict) -> float:
        """Calcula score para apenas observar"""
        score = 0.5  # Base: sempre observa um pouco
        
        # Personalidade observadora
        if personalidade.get("observadora", 0) > 0.7:
            score += 0.3
        
        # Curiosidade alta
        if emocional.get("curiosidade", 0) > 0.6:
            score += 0.2
        
        # Usuário presente mas não interagiu
        if situacional.get("usuario_presente") and not situacional.get("interacao_recente"):
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _score_mudar_humor(self, emocional: Dict) -> float:
        """Calcula score para mudar de humor"""
        score = 0.0
        
        # Irritação muito alta → quer mudar
        if emocional.get("irritacao", 0) > 0.7:
            score += 0.4
        
        # Energia muito baixa → quer mudar
        if emocional.get("energia", 0) < 0.2:
            score += 0.3
        
        return min(1.0, max(0.0, score))
    
    def _score_nada(self, emocional: Dict, situacional: Dict) -> float:
        """Calcula score para não fazer nada (importante!)"""
        score = 0.3  # Base: às vezes não faz nada
        
        # Tudo equilibrado → não precisa fazer nada
        necessidade = emocional.get("necessidade_social", 0)
        energia = emocional.get("energia", 0)
        
        if 0.3 < necessidade < 0.7 and 0.3 < energia < 0.7:
            score += 0.3
        
        # Usuário ausente → não faz nada
        if not situacional.get("usuario_presente"):
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _apply_randomness(self, scores: Dict) -> Dict:
        """Aplica imprevisibilidade controlada"""
        # Pequena variação aleatória (±10%)
        for key in scores:
            variation = (random.random() - 0.5) * 0.2
            scores[key] = scores[key] + variation
            scores[key] = max(0.0, min(1.0, scores[key]))
        return scores
    
    def _generate_motivo(self, tipo: DecisionType, emocional: Dict, situacional: Dict) -> str:
        """Gera motivo da decisão"""
        motivos = {
            DecisionType.FALAR: [
                "necessidade social alta",
                "usuário presente sem interação",
                "curiosidade ativa"
            ],
            DecisionType.SILENCIO: [
                "energia baixa",
                "personalidade reservada",
                "momento de descanso"
            ],
            DecisionType.OBSERVAR: [
                "personalidade observadora",
                "curiosidade sobre o ambiente",
                "aguardando momento certo"
            ],
            DecisionType.NADA: [
                "tudo equilibrado",
                "não há necessidade de ação",
                "momento de quietude"
            ]
        }
        
        if tipo in motivos:
            return random.choice(motivos[tipo])
        return "decisão autônoma"
