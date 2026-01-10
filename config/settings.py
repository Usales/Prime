"""
Configurações do Prime
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações da aplicação"""
    
    # Ambiente
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/prime.db")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma")
    
    # Sensorial
    CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
    ENABLE_CAMERA = os.getenv("ENABLE_CAMERA", "true").lower() == "true"
    ENABLE_MICROPHONE = os.getenv("ENABLE_MICROPHONE", "true").lower() == "true"
    
    # MQTT
    MQTT_ENABLED = os.getenv("MQTT_ENABLED", "false").lower() == "true"
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    
    # Personalidade (valores entre 0.0 e 1.0)
    PERSONALITY_AFETUOSA = float(os.getenv("PERSONALITY_AFETUOSA", "0.6"))
    PERSONALITY_OBSERVADORA = float(os.getenv("PERSONALITY_OBSERVADORA", "0.8"))
    PERSONALITY_IRONICA = float(os.getenv("PERSONALITY_IRONICA", "0.4"))
    PERSONALITY_RESERVADA = float(os.getenv("PERSONALITY_RESERVADA", "0.3"))
    PERSONALITY_CURIOSA = float(os.getenv("PERSONALITY_CURIOSA", "0.7"))
    
    # Sistema de Decisão
    TICK_INTERVAL = float(os.getenv("TICK_INTERVAL", "5.0"))
    DECISION_THRESHOLD = float(os.getenv("DECISION_THRESHOLD", "0.5"))
    
    # Logs
    LOG_FILE = os.getenv("LOG_FILE", "./logs/prime.log")
    LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))


settings = Settings()
