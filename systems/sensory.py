"""
Sistema Sensorial
Visão (presença) e Audição (palavras-chave)
Pipeline realista com ativação por movimento
"""

import cv2
import numpy as np
from typing import Optional, Dict, Callable
from datetime import datetime
import threading
import time


class SensorySystem:
    """
    Sistema sensorial com pipeline realista:
    Sensor de movimento → Ativa câmera → Detecta forma humana → Classifica contexto → Desliga câmera
    """
    
    def __init__(self, camera_index: int = 0, enabled: bool = True):
        self.camera_index = camera_index
        self.enabled = enabled
        self.camera = None
        self.is_processing = False
        self.last_detection = None
        self.presence_callback: Optional[Callable] = None
        
        # Estado atual
        self.current_presence = False
        self.current_user_state = "desconhecido"
        self.current_light_level = "desconhecida"
        
        # Thread de processamento
        self._thread: Optional[threading.Thread] = None
        self._stop_thread = False
    
    def set_presence_callback(self, callback: Callable):
        """Define callback para quando detectar presença"""
        self.presence_callback = callback
    
    def start(self):
        """Inicia sistema sensorial"""
        if not self.enabled:
            return
        
        if self._thread is None or not self._thread.is_alive():
            self._stop_thread = False
            self._thread = threading.Thread(target=self._sensory_loop, daemon=True)
            self._thread.start()
    
    def stop(self):
        """Para sistema sensorial"""
        self._stop_thread = True
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def _sensory_loop(self):
        """Loop principal de processamento sensorial"""
        while not self._stop_thread:
            try:
                # Simula detecção de movimento (por enquanto)
                # Em produção, usaria sensor PIR ou análise de frame
                movement_detected = self._check_movement()
                
                if movement_detected:
                    self._process_presence()
                else:
                    # Sem movimento, mantém estado
                    if self.current_presence:
                        # Verifica se ainda há presença (check periódico)
                        time.sleep(5)  # Espera 5 segundos antes de verificar novamente
                    else:
                        time.sleep(2)  # Sem presença, verifica menos frequentemente
                
                time.sleep(0.5)  # Pequeno delay entre ciclos
                
            except Exception as e:
                print(f"Erro no sistema sensorial: {e}")
                time.sleep(1)
    
    def _check_movement(self) -> bool:
        """
        Verifica se há movimento (simulado por enquanto)
        Em produção: sensor PIR ou análise de diferença de frames
        """
        # Por enquanto, simula detecção aleatória para teste
        # Em produção real, implementaria detecção real
        return False  # Desabilitado por padrão para não usar câmera sem necessidade
    
    def _process_presence(self):
        """Processa detecção de presença"""
        if self.camera is None:
            try:
                self.camera = cv2.VideoCapture(self.camera_index)
                if not self.camera.isOpened():
                    self.camera = None
                    return
            except Exception as e:
                print(f"Erro ao abrir câmera: {e}")
                return
        
        try:
            # Captura frame
            ret, frame = self.camera.read()
            if not ret:
                return
            
            # Detecta presença humana (simplificado)
            presence = self._detect_human_presence(frame)
            
            if presence != self.current_presence:
                self.current_presence = presence
                self.last_detection = datetime.now()
                
                # Classifica contexto
                self._classify_context(frame)
                
                # Chama callback
                if self.presence_callback:
                    self.presence_callback(presence, self.current_user_state)
            
            # Desliga câmera após processamento
            # (em produção, manteria aberta por um tempo mínimo)
            
        except Exception as e:
            print(f"Erro ao processar presença: {e}")
        finally:
            # Por enquanto, mantém câmera fechada quando não em uso
            # Em produção, otimizaria isso
            pass
    
    def _detect_human_presence(self, frame) -> bool:
        """
        Detecta presença humana no frame
        Por enquanto: simulado
        Em produção: MediaPipe ou YOLO
        """
        # Simulação: sempre retorna False por enquanto
        # Para não usar câmera sem configuração adequada
        return False
    
    def _classify_context(self, frame):
        """Classifica contexto do ambiente"""
        # Analisa luz (simplificado)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 50:
            self.current_light_level = "baixa"
        elif mean_brightness < 150:
            self.current_light_level = "media"
        else:
            self.current_light_level = "alta"
        
        # Estado do usuário (simulado por enquanto)
        # Em produção: análise de postura, movimento, etc.
        self.current_user_state = "normal"
    
    def get_current_state(self) -> Dict:
        """Retorna estado sensorial atual"""
        return {
            "presence": self.current_presence,
            "user_state": self.current_user_state,
            "light_level": self.current_light_level,
            "last_detection": self.last_detection.isoformat() if self.last_detection else None
        }
    
    def process_audio(self, audio_data) -> Dict:
        """
        Processa áudio (simplificado)
        Em produção: Whisper para transcrição + análise de tom
        """
        # Por enquanto retorna vazio
        # Em produção: transcreveria com Whisper e extrairia palavras-chave
        return {
            "text": "",
            "keywords": [],
            "emotional_tone": "neutral"
        }
