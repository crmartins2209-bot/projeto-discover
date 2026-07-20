#!/usr/bin/env python3
"""
Interface Gráfica para Macro Recorder
Interface simples para controlar gravação e reprodução de macros
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from macro_recorder import MacroRecorder
import threading

class MacroRecorderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro Recorder - TinyTask para Mac")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.recorder = MacroRecorder()
        self.recording_thread = None
        self.playback_thread = None
        
        self.create_widgets()
        
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Título
        title_label = tk.Label(
            self.root, 
            text="Macro Recorder", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botões de controle
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.record_btn = ttk.Button(
            control_frame, 
            text="Gravar", 
            command=self.toggle_recording
        )
        self.record_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.play_btn = ttk.Button(
            control_frame, 
            text="Reproduzir", 
            command=self.play_macro
        )
        self.play_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.stop_btn = ttk.Button(
            control_frame, 
            text="Parar", 
            command=self.stop_all,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Frame de configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        config_frame.pack(fill=tk.X, pady=10)
        
        # Velocidade
        speed_frame = ttk.Frame(config_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="Velocidade:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(
            speed_frame, 
            from_=0.1, 
            to=3.0, 
            variable=self.speed_var,
            orient=tk.HORIZONTAL
        )
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(side=tk.LEFT)
        self.speed_scale.configure(command=self.update_speed_label)
        
        # Loop
        self.loop_var = tk.BooleanVar(value=False)
        self.loop_check = ttk.Checkbutton(
            config_frame, 
            text="Reproduzir em loop", 
            variable=self.loop_var
        )
        self.loop_check.pack(anchor=tk.W, pady=5)
        
        # Frame de arquivos
        file_frame = ttk.LabelFrame(main_frame, text="Arquivo", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(
            file_frame, 
            text="Salvar Macro", 
            command=self.save_macro
        )
        save_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        load_btn = ttk.Button(
            file_frame, 
            text="Carregar Macro", 
            command=self.load_macro
        )
        load_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, text="Pronto", foreground="green")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Contador de eventos
        ttk.Label(status_frame, text="Eventos:").pack(side=tk.LEFT, padx=(20, 0))
        self.events_label = ttk.Label(status_frame, text="0")
        self.events_label.pack(side=tk.LEFT, padx=5)
        
        # Instruções
        instructions = tk.Label(
            main_frame,
            text="Dica: Pressione F9 durante a gravação para parar",
            font=("Arial", 8),
            foreground="gray"
        )
        instructions.pack(pady=10)
        
    def update_speed_label(self, value):
        """Atualiza o label de velocidade"""
        self.speed_label.config(text=f"{float(value):.1f}x")
        
    def toggle_recording(self):
        """Alterna entre gravar e parar gravação"""
        if not self.recorder.recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Inicia a gravação"""
        self.recorder.start_recording()
        self.record_btn.config(text="Parar Gravação")
        self.play_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Gravando...", foreground="red")
        self.update_events_count()
        
    def stop_recording(self):
        """Para a gravação"""
        self.recorder.stop_recording()
        self.record_btn.config(text="Gravar")
        self.play_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Pronto", foreground="green")
        self.update_events_count()
        
    def play_macro(self):
        """Reproduz a macro"""
        if not self.recorder.events:
            messagebox.showwarning("Aviso", "Nenhum evento gravado para reproduzir")
            return
            
        self.play_btn.config(state=tk.DISABLED)
        self.record_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Reproduzindo...", foreground="blue")
        
        speed = self.speed_var.get()
        loop = self.loop_var.get()
        
        self.playback_thread = threading.Thread(
            target=self.recorder.play_macro,
            kwargs={'speed_multiplier': speed, 'loop': loop}
        )
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
        # Verifica quando a reprodução termina
        self.root.after(100, self.check_playback_status)
        
    def check_playback_status(self):
        """Verifica se a reprodução terminou"""
        if not self.recorder.playing:
            self.play_btn.config(state=tk.NORMAL)
            self.record_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Pronto", foreground="green")
        else:
            self.root.after(100, self.check_playback_status)
            
    def stop_all(self):
        """Para todas as operações"""
        if self.recorder.recording:
            self.stop_recording()
        if self.recorder.playing:
            self.recorder.stop_playback_now()
            self.play_btn.config(state=tk.NORMAL)
            self.record_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Pronto", foreground="green")
            
    def save_macro(self):
        """Salva a macro em um arquivo"""
        if not self.recorder.events:
            messagebox.showwarning("Aviso", "Nenhum evento gravado para salvar")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.recorder.save_macro(filename)
            messagebox.showinfo("Sucesso", f"Macro salva em {filename}")
            
    def load_macro(self):
        """Carrega uma macro de um arquivo"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.recorder.load_macro(filename)
            self.update_events_count()
            messagebox.showinfo("Sucesso", f"Macro carregada de {filename}")
            
    def update_events_count(self):
        """Atualiza o contador de eventos"""
        self.events_label.config(text=str(len(self.recorder.events)))
        
    def on_closing(self):
        """Trata o fechamento da janela"""
        self.stop_all()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MacroRecorderGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()