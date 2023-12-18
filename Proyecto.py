import psutil
import tkinter as tk

def monitorear_cpu():
    uso_cpu = psutil.cpu_percent()

    if uso_cpu > 10:
        mensaje = f"Uso elevado de CPU: {uso_cpu}%"
        mostrar_ventana_flotante("Alerta de CPU", mensaje)

    ventana.after(5000, monitorear_cpu)

def monitorear_memoria():
    uso_memoria = psutil.virtual_memory().percent

    if uso_memoria > 60:
        mensaje = f"Uso elevado de Memoria: {uso_memoria}%"
        mostrar_ventana_flotante("Alerta de Memoria", mensaje)

    ventana.after(5000, monitorear_memoria)

def mostrar_ventana_flotante(titulo, mensaje):
    ventana_alerta = tk.Toplevel(ventana)
    ventana_alerta.title(titulo)
    
    etiqueta = tk.Label(ventana_alerta, text=mensaje, padx=20, pady=20)
    etiqueta.pack()

    boton_cerrar = tk.Button(ventana_alerta, text="Cerrar", command=ventana_alerta.destroy)
    boton_cerrar.pack()

ventana = tk.Tk()
ventana.title("Monitoreo de Sistema")

monitorear_cpu()
monitorear_memoria()

ventana.mainloop()