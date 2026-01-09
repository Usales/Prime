"""
Prime Core - Orquestrador Principal
Conecta todos os 7 sistemas e executa o loop principal
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional

from systems.situational_awareness import SituationalAwareness
from systems.emotional_system import EmotionalSystem
from systems.personality import PersonalitySystem, PersonalityTraits
from systems.memory import MemorySystem, MemoryEvent
from systems.sensory import SensorySystem
from systems.decision import DecisionSystem, DecisionType
from systems.expression import ExpressionSystem
from config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PrimeCore:
    """
    Núcleo do agente Prime
    Orquestra todos os sistemas
    """
    
    def __init__(self):
        # Inicializa todos os sistemas
        logger.info("Inicializando sistemas do Prime...")
        
        # 1. Consciência Situacional
        self.situational = SituationalAwareness()
        
        # 2. Sistema Emocional
        self.emotional = EmotionalSystem()
        
        # 3. Personalidade
        traits = PersonalityTraits(
            afetuosa=settings.PERSONALITY_AFETUOSA,
            observadora=settings.PERSONALITY_OBSERVADORA,
            ironica=settings.PERSONALITY_IRONICA,
            reservada=settings.PERSONALITY_RESERVADA,
            curiosa=settings.PERSONALITY_CURIOSA
        )
        self.personality = PersonalitySystem(traits)
        
        # 4. Memória
        self.memory = MemorySystem(settings.DATABASE_PATH)
        
        # 5. Sensorial
        self.sensory = SensorySystem(
            camera_index=settings.CAMERA_INDEX,
            enabled=settings.ENABLE_CAMERA
        )
        self.sensory.set_presence_callback(self._on_presence_detected)
        
        # 6. Decisão
        self.decision = DecisionSystem()
        
        # 7. Expressão
        self.expression = ExpressionSystem(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        
        # Estado interno
        self.is_running = False
        self.last_decision: Optional[dict] = None
        self.tick_count = 0
    
    async def initialize(self):
        """Inicializa sistemas assíncronos"""
        logger.info("Inicializando sistemas assíncronos...")
        await self.memory.initialize()
        logger.info("Sistemas inicializados!")
    
    def _on_presence_detected(self, presente: bool, estado: str):
        """Callback quando detecta presença"""
        self.situational.update_presence(presente)
        if estado != "desconhecido":
            self.situational.update_user_state(estado)
        
        # Atualiza luz do ambiente
        sensory_state = self.sensory.get_current_state()
        if sensory_state.get("light_level") != "desconhecida":
            self.situational.update_light(sensory_state["light_level"])
        
        logger.info(f"Presença detectada: {presente}, Estado: {estado}")
    
    async def tick(self):
        """
        Ciclo principal de execução
        Executado a cada poucos segundos
        """
        self.tick_count += 1
        
        # 1. Atualiza consciência situacional
        self.situational.tick()
        situacional_state = self.situational.get_state_dict()
        
        # 2. Atualiza sistema emocional (homeostase)
        self.emotional.tick(situacional_state)
        emocional_state = self.emotional.get_state_dict()
        
        # 3. Obtém memória recente
        memoria_recente = await self.memory.get_recent_events(limit=5)
        
        # 4. Toma decisão
        decisao = self.decision.decide(
            emocional=emocional_state,
            situacional=situacional_state,
            personalidade=self.personality.get_traits_dict(),
            memoria_recente=[m for m in memoria_recente]
        )
        
        self.last_decision = decisao.to_dict()
        
        # 5. Executa decisão
        await self._execute_decision(decisao, emocional_state, situacional_state, memoria_recente)
        
        # Log periódico
        if self.tick_count % 10 == 0:
            logger.debug(f"Tick {self.tick_count} - Decisão: {decisao.tipo.value}")
    
    async def _execute_decision(self, decisao, emocional: dict, situacional: dict, 
                                memoria_recente: list):
        """Executa a decisão tomada"""
        if decisao.tipo == DecisionType.FALAR:
            await self._execute_falar(decisao, emocional, situacional, memoria_recente)
        elif decisao.tipo == DecisionType.SILENCIO:
            await self._execute_silenciar()
        elif decisao.tipo == DecisionType.OBSERVAR:
            await self._execute_observar()
        elif decisao.tipo == DecisionType.NADA:
            # Não faz nada - isso é válido!
            pass
    
    async def _execute_falar(self, decisao, emocional: dict, situacional: dict, 
                            memoria_recente: list):
        """Executa decisão de falar"""
        # Gera resposta usando sistema de expressão
        resposta = self.expression.generate_response(
            decisao=decisao.to_dict(),
            personalidade=self.personality.get_traits_dict(),
            emocional=emocional,
            situacional=situacional,
            memoria_recente=memoria_recente
        )
        
        if resposta:
            logger.info(f"Prime fala: {resposta}")
            
            # Fala usando TTS
            self.expression.speak(resposta, async_mode=True)
            
            # Marca interação
            self.situational.mark_interaction(True)
            
            # Registra na memória
            evento = MemoryEvent(
                tipo="interacao",
                evento="falei",
                resposta_dada=resposta,
                resultado="aceita",  # Será atualizado depois
                peso_emocional=decisao.intensidade,
                contexto={
                    "decisao": decisao.motivo,
                    "emocional": emocional
                }
            )
            await self.memory.store_event(evento)
            
            # Atualiza emoção (interação positiva reduz necessidade social)
            self.emotional.on_interaction("normal")
        else:
            # Decidiu falar mas não gerou texto (imperfeição controlada)
            logger.debug("Decidiu falar mas ficou em silêncio (imperfeição)")
    
    async def _execute_silenciar(self):
        """Executa decisão de silêncio"""
        logger.debug("Prime escolheu silêncio")
        # Não faz nada - silêncio é uma ação válida
    
    async def _execute_observar(self):
        """Executa decisão de observar"""
        logger.debug("Prime está observando")
        # Apenas observa - não faz nada além de atualizar estados
    
    async def run(self, tick_interval: float = 5.0):
        """
        Loop principal de execução
        tick_interval: segundos entre cada tick
        """
        logger.info("Iniciando Prime Core...")
        await self.initialize()
        
        # Inicia sistema sensorial
        self.sensory.start()
        
        self.is_running = True
        logger.info(f"Prime está vivo! Tick a cada {tick_interval}s")
        
        try:
            while self.is_running:
                await self.tick()
                await asyncio.sleep(tick_interval)
        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}", exc_info=True)
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Encerra sistemas"""
        logger.info("Encerrando Prime...")
        self.is_running = False
        self.sensory.stop()
        logger.info("Prime encerrado.")
    
    def get_status(self) -> dict:
        """Retorna status atual de todos os sistemas"""
        return {
            "running": self.is_running,
            "tick_count": self.tick_count,
            "situational": self.situational.get_state_dict(),
            "emotional": self.emotional.get_state_dict(),
            "personality": self.personality.get_traits_dict(),
            "last_decision": self.last_decision,
            "sensory": self.sensory.get_current_state()
        }
