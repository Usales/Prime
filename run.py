"""
Script simples para executar Prime sem FastAPI
Útil para testes e desenvolvimento
"""

import asyncio
import logging
from prime_core import PrimeCore
from config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Executa Prime em modo standalone"""
    logger.info("=" * 50)
    logger.info("Iniciando Prime - Agente Vivo")
    logger.info("=" * 50)
    
    prime = PrimeCore()
    
    try:
        await prime.run(tick_interval=5.0)
    except KeyboardInterrupt:
        logger.info("\nInterrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
