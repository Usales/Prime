"""
Prime - Agente Vivo
Ponto de entrada principal
"""

import asyncio
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn

from prime_core import PrimeCore
from config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cria aplicação FastAPI
app = FastAPI(
    title="Prime - Agente Vivo",
    description="Sistema de agente vivo com 7 sistemas independentes",
    version="0.1.0"
)

# Instância global do Prime
prime: PrimeCore = None
prime_task: asyncio.Task = None


@app.on_event("startup")
async def startup():
    """Inicializa Prime na startup"""
    global prime, prime_task
    
    logger.info("Iniciando Prime...")
    prime = PrimeCore()
    await prime.initialize()
    
    # Inicia loop principal em background
    prime_task = asyncio.create_task(prime.run(tick_interval=5.0))
    logger.info("Prime iniciado!")


@app.on_event("shutdown")
async def shutdown():
    """Encerra Prime no shutdown"""
    global prime, prime_task
    
    if prime:
        await prime.shutdown()
    if prime_task:
        prime_task.cancel()
        try:
            await prime_task
        except asyncio.CancelledError:
            pass
    
    logger.info("Prime encerrado.")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "name": "Prime",
        "status": "alive",
        "description": "Agente vivo com 7 sistemas independentes",
        "version": "0.1.0",
        "endpoints": {
            "/status": "Status completo de todos os sistemas",
            "/health": "Health check rápido",
            "/interaction": "Registra interação do usuário"
        }
    }


@app.get("/status")
async def get_status():
    """Retorna status completo do Prime"""
    if not prime:
        return JSONResponse(
            status_code=503,
            content={"error": "Prime não está inicializado"}
        )
    
    return prime.get_status()


@app.get("/health")
async def health():
    """Health check"""
    if not prime or not prime.is_running:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy"}
        )
    
    return {"status": "healthy"}


@app.post("/interaction")
async def register_interaction(tipo: str = "normal"):
    """
    Registra interação do usuário
    tipo: "normal", "positiva", "negativa", "ignorada"
    """
    if not prime:
        return JSONResponse(
            status_code=503,
            content={"error": "Prime não está inicializado"}
        )
    
    # Atualiza sistema emocional
    prime.emotional.on_interaction(tipo)
    
    # Marca interação recente
    prime.situational.mark_interaction(True)
    
    return {"status": "interaction_registered", "tipo": tipo}


if __name__ == "__main__":
    # Executa servidor
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
