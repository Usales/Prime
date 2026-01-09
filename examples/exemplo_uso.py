"""
Exemplo de uso dos sistemas do Prime
Demonstra como cada sistema funciona independentemente
"""

import asyncio
from systems.situational_awareness import SituationalAwareness
from systems.emotional_system import EmotionalSystem
from systems.personality import PersonalitySystem, PersonalityTraits
from systems.decision import DecisionSystem, DecisionType
from systems.memory import MemorySystem, MemoryEvent
from datetime import datetime


async def exemplo_consciencia_situacional():
    """Exemplo do sistema de consciência situacional"""
    print("\n=== Sistema de Consciência Situacional ===")
    
    situacional = SituationalAwareness()
    
    # Atualiza estados
    situacional.update_presence(True)
    situacional.update_user_state("cansado")
    situacional.update_light("baixa")
    situacional.update_environment("silencioso")
    
    print("Estado atual:")
    print(situacional.get_state().to_json())


def exemplo_sistema_emocional():
    """Exemplo do sistema emocional"""
    print("\n=== Sistema Emocional ===")
    
    emocional = EmotionalSystem()
    situacional_state = {
        "usuario_presente": True,
        "usuario_estado": "cansado",
        "interacao_recente": False,
        "ambiente": "silencioso"
    }
    
    # Simula alguns ticks
    print("Estado inicial:")
    print(emocional.get_state_dict())
    
    for i in range(5):
        emocional.tick(situacional_state)
        print(f"\nApós tick {i+1}:")
        print(emocional.get_state_dict())
    
    # Reage a interação
    print("\nApós interação positiva:")
    emocional.on_interaction("positiva")
    print(emocional.get_state_dict())


def exemplo_personalidade():
    """Exemplo do sistema de personalidade"""
    print("\n=== Sistema de Personalidade ===")
    
    traits = PersonalityTraits(
        afetuosa=0.6,
        observadora=0.8,
        ironica=0.4,
        reservada=0.3,
        curiosa=0.7
    )
    
    personalidade = PersonalitySystem(traits)
    
    print("Traços:")
    print(personalidade.get_traits_dict())
    
    print("\nConstraints para LLM:")
    print(personalidade.get_llm_constraints())


def exemplo_decisao():
    """Exemplo do sistema de decisão"""
    print("\n=== Sistema de Decisão ===")
    
    decisao = DecisionSystem()
    
    emocional = {
        "energia": 0.4,
        "curiosidade": 0.7,
        "necessidade_social": 0.8,
        "irritacao": 0.1,
        "apego": 0.3
    }
    
    situacional = {
        "usuario_presente": True,
        "usuario_estado": "normal",
        "interacao_recente": False,
        "ambiente": "silencioso"
    }
    
    personalidade = {
        "afetuosa": 0.6,
        "observadora": 0.8,
        "reservada": 0.3,
        "curiosa": 0.7
    }
    
    resultado = decisao.decide(emocional, situacional, personalidade)
    
    print(f"Decisão: {resultado.tipo.value}")
    print(f"Intensidade: {resultado.intensidade:.2f}")
    print(f"Motivo: {resultado.motivo}")
    print(f"\nScores:")
    for tipo, score in resultado.contexto.get("scores", {}).items():
        print(f"  {tipo}: {score:.2f}")


async def exemplo_memoria():
    """Exemplo do sistema de memória"""
    print("\n=== Sistema de Memória ===")
    
    memoria = MemorySystem("./data/exemplo.db")
    await memoria.initialize()
    
    # Armazena alguns eventos
    evento1 = MemoryEvent(
        tipo="interacao",
        evento="usuário chegou cansado",
        resposta_dada="silenciosa",
        resultado="aceita",
        peso_emocional=0.7
    )
    
    evento2 = MemoryEvent(
        tipo="interacao",
        evento="falei algo",
        resposta_dada="olá",
        resultado="positiva",
        peso_emocional=0.5
    )
    
    await memoria.store_event(evento1)
    await memoria.store_event(evento2)
    
    # Recupera eventos recentes
    recentes = await memoria.get_recent_events(limit=5)
    print(f"Eventos recentes: {len(recentes)}")
    for evento in recentes:
        print(f"  - {evento.evento} (peso: {evento.peso_emocional})")
    
    # Recupera memórias emocionais
    emocionais = await memoria.get_emotional_memories(min_weight=0.6)
    print(f"\nMemórias emocionais: {len(emocionais)}")
    for mem in emocionais:
        print(f"  - {mem.evento} (peso: {mem.peso_emocional})")


async def exemplo_completo():
    """Exemplo completo integrando todos os sistemas"""
    print("\n=== Exemplo Completo ===")
    
    # Inicializa sistemas
    situacional = SituationalAwareness()
    emocional = EmotionalSystem()
    personalidade = PersonalitySystem()
    decisao = DecisionSystem()
    memoria = MemorySystem("./data/exemplo_completo.db")
    await memoria.initialize()
    
    # Simula cenário: usuário chega cansado
    print("\n1. Usuário chega cansado...")
    situacional.update_presence(True)
    situacional.update_user_state("cansado")
    situacional.update_light("baixa")
    
    # Atualiza emoções
    for _ in range(3):
        emocional.tick(situacional.get_state_dict())
    
    print("Estado emocional:")
    print(emocional.get_state_dict())
    
    # Toma decisão
    print("\n2. Tomando decisão...")
    resultado = decisao.decide(
        emocional.get_state_dict(),
        situacional.get_state_dict(),
        personalidade.get_traits_dict()
    )
    
    print(f"Decisão: {resultado.tipo.value}")
    print(f"Motivo: {resultado.motivo}")
    
    # Registra na memória
    if resultado.tipo == DecisionType.FALAR:
        evento = MemoryEvent(
            tipo="interacao",
            evento="usuário chegou cansado",
            resposta_dada="decidiu falar",
            resultado="aceita",
            peso_emocional=resultado.intensidade
        )
        await memoria.store_event(evento)
        print("\n3. Evento armazenado na memória")


async def main():
    """Executa todos os exemplos"""
    print("=" * 60)
    print("EXEMPLOS DE USO - PRIME")
    print("=" * 60)
    
    await exemplo_consciencia_situacional()
    exemplo_sistema_emocional()
    exemplo_personalidade()
    exemplo_decisao()
    await exemplo_memoria()
    await exemplo_completo()
    
    print("\n" + "=" * 60)
    print("Exemplos concluídos!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
