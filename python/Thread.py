import threading
import queue
from tkinter import messagebox
import time

# ====== CLASE PARA MANEJAR TAREAS EN SEGUNDO PLANO ======
class TareaThread(threading.Thread):
    """Thread que ejecuta una función y guarda el resultado en una cola"""
    def __init__(self, target, args=(), kwargs=None, callback=None, error_callback=None):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs if kwargs else {}
        self.callback = callback
        self.error_callback = error_callback
        self.resultado = None
        self.error = None
        self.daemon = True  # El thread se cierra cuando se cierra la app
    
    def run(self):
        try:
            self.resultado = self.target(*self.args, **self.kwargs)
            if self.callback:
                self.callback(self.resultado)
        except Exception as e:
            self.error = e
            if self.error_callback:
                self.error_callback(e)