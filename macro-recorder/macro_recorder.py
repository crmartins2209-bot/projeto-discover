#!/usr/bin/env python3
"""
Macro Recorder - Gravador e reprodutor de macros para macOS
Similar ao TinyTask, grava ações de mouse e teclado e permite reproduzir
"""

import time
import json
import threading
from pynput import mouse, keyboard
from pynput.mouse import Button
import pyautogui

class MacroRecorder:
    def __init__(self):
        self.recording = False
        self.playing = False
        self.events = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.stop_playback = False
        
    def start_recording(self):
        """Inicia a gravação de eventos"""
        self.recording = True
        self.events = []
        self.start_time = time.time()
        
        # Inicia listeners
        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll,
            on_move=self.on_mouse_move
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        print("Gravação iniciada... Pressione F9 para parar")
        
    def stop_recording(self):
        """Para a gravação"""
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print(f"Gravação parada. {len(self.events)} eventos gravados.")
        
    def on_mouse_click(self, x, y, button, pressed):
        """Captura cliques do mouse"""
        if not self.recording:
            return
        timestamp = time.time() - self.start_time
        self.events.append({
            'type': 'mouse_click',
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed,
            'timestamp': timestamp
        })
        
    def on_mouse_scroll(self, x, y, dx, dy):
        """Captura scroll do mouse"""
        if not self.recording:
            return
        timestamp = time.time() - self.start_time
        self.events.append({
            'type': 'mouse_scroll',
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy,
            'timestamp': timestamp
        })
        
    def on_mouse_move(self, x, y):
        """Captura movimento do mouse"""
        if not self.recording:
            return
        timestamp = time.time() - self.start_time
        self.events.append({
            'type': 'mouse_move',
            'x': x,
            'y': y,
            'timestamp': timestamp
        })
        
    def on_key_press(self, key):
        """Captura pressionamento de tecla"""
        if not self.recording:
            return
        timestamp = time.time() - self.start_time
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        
        self.events.append({
            'type': 'key_press',
            'key': key_char,
            'timestamp': timestamp
        })
        
    def on_key_release(self, key):
        """Captura soltura de tecla"""
        if not self.recording:
            return
        timestamp = time.time() - self.start_time
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        
        self.events.append({
            'type': 'key_release',
            'key': key_char,
            'timestamp': timestamp
        })
        
    def play_macro(self, speed_multiplier=1.0, loop=False):
        """Reproduz a macro gravada"""
        if not self.events:
            print("Nenhum evento gravado para reproduzir")
            return
            
        self.playing = True
        self.stop_playback = False
        
        while self.playing and (loop or not self.stop_playback):
            last_timestamp = 0
            
            for event in self.events:
                if self.stop_playback:
                    break
                    
                delay = (event['timestamp'] - last_timestamp) / speed_multiplier
                if delay > 0:
                    time.sleep(delay)
                    
                last_timestamp = event['timestamp']
                
                try:
                    if event['type'] == 'mouse_click':
                        button = Button.left if event['button'] == 'Button.left' else Button.right
                        if event['pressed']:
                            pyautogui.mouseDown(button=button)
                        else:
                            pyautogui.mouseUp(button=button)
                            
                    elif event['type'] == 'mouse_scroll':
                        pyautogui.scroll(event['dy'], x=event['x'], y=event['y'])
                        
                    elif event['type'] == 'mouse_move':
                        pyautogui.moveTo(event['x'], event['y'])
                        
                    elif event['type'] == 'key_press':
                        self._press_key(event['key'])
                        
                    elif event['type'] == 'key_release':
                        self._release_key(event['key'])
                        
                except Exception as e:
                    print(f"Erro ao reproduzir evento: {e}")
                    
            if not loop:
                break
                
        self.playing = False
        print("Reprodução finalizada")
        
    def _press_key(self, key):
        """Pressiona uma tecla"""
        if key.startswith('Key.'):
            key_name = key.replace('Key.', '')
            pyautogui.keyDown(key_name.lower())
        elif key.startswith('KeyCode.'):
            # Teclas especiais
            key_map = {
                'space': 'space',
                'enter': 'enter',
                'tab': 'tab',
                'backspace': 'backspace',
                'delete': 'delete',
                'esc': 'esc',
                'shift': 'shift',
                'ctrl': 'ctrl',
                'cmd': 'command',
                'alt': 'alt'
            }
            key_name = key.replace('KeyCode.', '').lower()
            if key_name in key_map:
                pyautogui.keyDown(key_map[key_name])
        else:
            pyautogui.keyDown(key)
            
    def _release_key(self, key):
        """Solta uma tecla"""
        if key.startswith('Key.'):
            key_name = key.replace('Key.', '')
            pyautogui.keyUp(key_name.lower())
        elif key.startswith('KeyCode.'):
            key_map = {
                'space': 'space',
                'enter': 'enter',
                'tab': 'tab',
                'backspace': 'backspace',
                'delete': 'delete',
                'esc': 'esc',
                'shift': 'shift',
                'ctrl': 'ctrl',
                'cmd': 'command',
                'alt': 'alt'
            }
            key_name = key.replace('KeyCode.', '').lower()
            if key_name in key_map:
                pyautogui.keyUp(key_map[key_name])
        else:
            pyautogui.keyUp(key)
            
    def save_macro(self, filename):
        """Salva a macro em um arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=2)
        print(f"Macro salva em {filename}")
        
    def load_macro(self, filename):
        """Carrega uma macro de um arquivo JSON"""
        with open(filename, 'r') as f:
            self.events = json.load(f)
        print(f"Macro carregada de {filename} - {len(self.events)} eventos")
        
    def stop_playback_now(self):
        """Para a reprodução imediatamente"""
        self.stop_playback = True
        self.playing = False