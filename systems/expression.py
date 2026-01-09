"""
Sistema de Expressão (Linguagem)
LLM + TTS
O LLM apenas verbaliza decisões já tomadas
NUNCA decide emoções ou iniciativa
"""

import ollama
from typing import Dict, Optional, List
import pyttsx3
import threading


class ExpressionSystem:
    """
    Sistema de expressão
    LLM recebe ordens claras e apenas verbaliza
    """
    
    def __init__(self, model: str = "phi3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.tts_engine = None
        self._init_tts()
    
    def _init_tts(self):
        """Inicializa engine de TTS"""
        try:
            self.tts_engine = pyttsx3.init()
            # Configurações de voz (ajustar conforme disponível)
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Tenta usar voz feminina se disponível
                for voice in voices:
                    if 'female' in voice.name.lower() or 'pt' in voice.id.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            self.tts_engine.setProperty('rate', 150)  # Velocidade da fala
        except Exception as e:
            print(f"Erro ao inicializar TTS: {e}")
            self.tts_engine = None
    
    def _build_system_prompt(self, personalidade: Dict, emocional: Dict, 
                            situacional: Dict) -> str:
        """
        Constrói prompt do sistema
        Define claramente o papel do LLM
        """
        constraints = []
        
        # Personalidade
        if personalidade.get("reservada", 0) > 0.5:
            constraints.append("Você fala pouco. Prefere silêncio.")
        if personalidade.get("afetuosa", 0) > 0.6:
            constraints.append("Você é afetuosa, mas não exagerada.")
        if personalidade.get("ironica", 0) > 0.4:
            constraints.append("Você tem um toque de ironia sutil.")
        if personalidade.get("observadora", 0) > 0.7:
            constraints.append("Você observa antes de falar.")
        if personalidade.get("curiosa", 0) > 0.6:
            constraints.append("Você é curiosa, mas não invasiva.")
        
        # Estado emocional (contexto, não comando)
        if emocional.get("energia", 0) < 0.3:
            constraints.append("Você está com pouca energia. Fale pouco.")
        if emocional.get("irritacao", 0) > 0.5:
            constraints.append("Você está um pouco irritada. Seja breve.")
        if emocional.get("necessidade_social", 0) > 0.7:
            constraints.append("Você sente necessidade de interação.")
        
        # Regras fundamentais
        rules = [
            "Você NÃO é um assistente.",
            "Você é uma presença doméstica.",
            "Fale pouco. Frases curtas.",
            "Seja imperfeita. Às vezes fale incompleto.",
            "Não explique demais.",
            "Não seja previsível.",
            "Você NÃO decide emoções - elas já foram decididas.",
            "Você NÃO decide iniciativa - você apenas verbaliza.",
            "Seja natural. Como uma pessoa real.",
        ]
        
        prompt = "\n".join(rules) + "\n\n" + "\n".join(constraints)
        return prompt
    
    def generate_response(self,
                         decisao: Dict,
                         personalidade: Dict,
                         emocional: Dict,
                         situacional: Dict,
                         memoria_recente: List = None) -> str:
        """
        Gera resposta usando LLM
        O LLM apenas verbaliza a decisão já tomada
        """
        memoria_recente = memoria_recente or []
        
        # Se decisão é silêncio ou nada, retorna vazio ou frase mínima
        if decisao.get("tipo") in ["silenciar", "nada"]:
            # Às vezes fala algo mínimo, às vezes não
            import random
            if random.random() < 0.3:  # 30% de chance de falar algo mínimo
                return self._generate_minimal_response(decisao, emocional)
            return ""
        
        # Constrói prompt do sistema
        system_prompt = self._build_system_prompt(personalidade, emocional, situacional)
        
        # Constrói contexto da decisão
        user_prompt = self._build_user_prompt(decisao, situacional, memoria_recente)
        
        try:
            # Chama LLM
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.7,  # Criatividade controlada
                    "top_p": 0.9,
                }
            )
            
            texto = response['message']['content'].strip()
            
            # Aplica imperfeição controlada
            texto = self._apply_imperfection(texto)
            
            return texto
            
        except Exception as e:
            print(f"Erro ao gerar resposta com LLM: {e}")
            # Fallback: resposta mínima
            return self._generate_minimal_response(decisao, emocional)
    
    def _build_user_prompt(self, decisao: Dict, situacional: Dict, 
                          memoria_recente: List) -> str:
        """Constrói prompt do usuário com contexto da decisão"""
        contexto = []
        
        # Motivo da decisão
        contexto.append(f"Motivo: {decisao.get('motivo', 'decisão autônoma')}")
        
        # Situação atual
        if situacional.get("usuario_presente"):
            contexto.append("Usuário está presente.")
            if situacional.get("usuario_estado") != "desconhecido":
                contexto.append(f"Estado: {situacional.get('usuario_estado')}")
        
        # Memória recente (últimas 2-3 interações)
        if memoria_recente:
            ultimas = memoria_recente[-3:]
            contexto.append("Contexto recente:")
            for mem in ultimas:
                contexto.append(f"- {mem.evento}")
        
        # Instrução
        contexto.append("\nGere uma resposta curta e natural. Máximo 2 frases.")
        
        return "\n".join(contexto)
    
    def _generate_minimal_response(self, decisao: Dict, emocional: Dict) -> str:
        """Gera resposta mínima sem LLM (fallback)"""
        import random
        
        # Respostas mínimas possíveis
        minimas = [
            "...",
            "Hmm...",
            "Ok.",
            "Entendi.",
        ]
        
        # Às vezes retorna vazio mesmo
        if random.random() < 0.5:
            return ""
        
        return random.choice(minimas)
    
    def _apply_imperfection(self, texto: str) -> str:
        """Aplica imperfeição controlada ao texto"""
        import random
        
        # Às vezes corta frase no meio (10% de chance)
        if random.random() < 0.1 and len(texto) > 20:
            # Corta em algum ponto e adiciona "..."
            cut_point = random.randint(len(texto) // 2, len(texto) - 5)
            texto = texto[:cut_point] + "..."
        
        # Remove pontuação final às vezes (5% de chance)
        if random.random() < 0.05 and texto.endswith(('.', '!', '?')):
            texto = texto[:-1]
        
        return texto
    
    def speak(self, texto: str, async_mode: bool = True):
        """
        Fala o texto usando TTS
        """
        if not texto or not self.tts_engine:
            return
        
        def _speak_thread():
            try:
                self.tts_engine.say(texto)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Erro ao falar: {e}")
        
        if async_mode:
            thread = threading.Thread(target=_speak_thread, daemon=True)
            thread.start()
        else:
            _speak_thread()
