"""
Sistema de Memória Viva
Armazena eventos com peso emocional
Diferencia memória de curto, médio e longo prazo
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json
import aiosqlite
import os


@dataclass
class MemoryEvent:
    """Evento armazenado na memória"""
    id: Optional[int] = None
    timestamp: datetime = None
    tipo: str = ""  # "interacao", "presenca", "evento_emocional"
    evento: str = ""
    resposta_dada: str = ""
    resultado: str = ""  # "aceita", "ignorada", "negativa"
    peso_emocional: float = 0.5
    contexto: Dict = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.contexto is None:
            self.contexto = {}


class MemorySystem:
    """
    Sistema de memória com três níveis:
    - Curto prazo: últimas falas e emoções
    - Médio prazo: hábitos e padrões
    - Longo prazo: momentos marcantes
    """
    
    def __init__(self, db_path: str = "./data/prime.db"):
        self.db_path = db_path
        self._ensure_db_dir()
        self._short_term: List[MemoryEvent] = []  # Últimas 20 interações
        self._max_short_term = 20
    
    def _ensure_db_dir(self):
        """Garante que o diretório do banco existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    async def initialize(self):
        """Inicializa banco de dados"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memory_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    evento TEXT NOT NULL,
                    resposta_dada TEXT,
                    resultado TEXT,
                    peso_emocional REAL DEFAULT 0.5,
                    contexto TEXT
                )
            """)
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON memory_events(timestamp)
            """)
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_tipo ON memory_events(tipo)
            """)
            await db.commit()
    
    async def store_event(self, event: MemoryEvent):
        """Armazena evento na memória"""
        # Adiciona à memória de curto prazo
        self._short_term.append(event)
        if len(self._short_term) > self._max_short_term:
            self._short_term.pop(0)
        
        # Armazena no banco (médio e longo prazo)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO memory_events 
                (timestamp, tipo, evento, resposta_dada, resultado, peso_emocional, contexto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event.timestamp.isoformat(),
                event.tipo,
                event.evento,
                event.resposta_dada,
                event.resultado,
                event.peso_emocional,
                json.dumps(event.contexto)
            ))
            await db.commit()
    
    async def get_recent_events(self, limit: int = 10) -> List[MemoryEvent]:
        """Retorna eventos recentes (curto prazo)"""
        return self._short_term[-limit:]
    
    async def get_events_by_type(self, tipo: str, days: int = 30) -> List[MemoryEvent]:
        """Retorna eventos de um tipo específico"""
        cutoff = datetime.now() - timedelta(days=days)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM memory_events 
                WHERE tipo = ? AND timestamp > ?
                ORDER BY timestamp DESC
            """, (tipo, cutoff.isoformat())) as cursor:
                rows = await cursor.fetchall()
                events = []
                for row in rows:
                    event = MemoryEvent(
                        id=row['id'],
                        timestamp=datetime.fromisoformat(row['timestamp']),
                        tipo=row['tipo'],
                        evento=row['evento'],
                        resposta_dada=row['resposta_dada'] or "",
                        resultado=row['resultado'] or "",
                        peso_emocional=row['peso_emocional'],
                        contexto=json.loads(row['contexto'] or '{}')
                    )
                    events.append(event)
                return events
    
    async def get_emotional_memories(self, min_weight: float = 0.7) -> List[MemoryEvent]:
        """Retorna memórias com alto peso emocional (longo prazo)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM memory_events 
                WHERE peso_emocional >= ?
                ORDER BY peso_emocional DESC, timestamp DESC
                LIMIT 50
            """, (min_weight,)) as cursor:
                rows = await cursor.fetchall()
                events = []
                for row in rows:
                    event = MemoryEvent(
                        id=row['id'],
                        timestamp=datetime.fromisoformat(row['timestamp']),
                        tipo=row['tipo'],
                        evento=row['evento'],
                        resposta_dada=row['resposta_dada'] or "",
                        resultado=row['resultado'] or "",
                        peso_emocional=row['peso_emocional'],
                        contexto=json.loads(row['contexto'] or '{}')
                    )
                    events.append(event)
                return events
    
    async def get_patterns(self, days: int = 7) -> Dict:
        """Identifica padrões recorrentes (médio prazo)"""
        cutoff = datetime.now() - timedelta(days=days)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT tipo, resultado, COUNT(*) as count
                FROM memory_events
                WHERE timestamp > ?
                GROUP BY tipo, resultado
                ORDER BY count DESC
            """, (cutoff.isoformat(),)) as cursor:
                rows = await cursor.fetchall()
                patterns = {}
                for row in rows:
                    key = f"{row['tipo']}_{row['resultado']}"
                    patterns[key] = row['count']
                return patterns
    
    def get_short_term_memory(self) -> List[MemoryEvent]:
        """Retorna memória de curto prazo (sem async)"""
        return self._short_term.copy()
