import psutil
import tkinter as tk
from threading import Thread
import time

UMBRAL_CPU = 10
UMBRAL_MEMORIA = 60

class VentanaFlotante(tk.Toplevel):
    def __init__(self):
        super().__init__(ventana)
        self.title("Alerta del Sistema")
        self.etiqueta_cpu = tk.Label(self, text="", padx=20, pady=20)
        self.etiqueta_memoria = tk.Label(self, text="", padx=20, pady=20)
        self.etiqueta_cpu.pack()
        self.etiqueta_memoria.pack()

        boton_cerrar = tk.Button(self, text="Cerrar", command=self.destroy)
        boton_cerrar.pack()

def monitorear_cpu(ventana_flotante):
    while True:
        uso_cpu = psutil.cpu_percent()

        if uso_cpu > UMBRAL_CPU:
            mensaje_cpu = f"Uso elevado de CPU: {uso_cpu}%\n Cierre algunas aplicaciones"
            ventana_flotante.etiqueta_cpu.config(text=mensaje_cpu)

        time.sleep(5)

def monitorear_memoria(ventana_flotante):
    while True:
        uso_memoria = psutil.virtual_memory().percent

        if uso_memoria > UMBRAL_MEMORIA:
            mensaje_memoria = f"Uso elevado de Memoria: {uso_memoria}%\n Cierre algunas aplicaciones"
            ventana_flotante.etiqueta_memoria.config(text=mensaje_memoria)

        time.sleep(5)

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Monitoreo de Sistema")

    ventana_flotante = VentanaFlotante()

    # Iniciar hilos para el monitoreo en segundo plano
    hilo_cpu = Thread(target=monitorear_cpu, args=(ventana_flotante,), daemon=True)
    hilo_memoria = Thread(target=monitorear_memoria, args=(ventana_flotante,), daemon=True)

    hilo_cpu.start()
    hilo_memoria.start()

    ventana.mainloop()

