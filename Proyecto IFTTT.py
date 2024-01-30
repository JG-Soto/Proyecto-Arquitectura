import psutil
import tkinter as tk
from threading import Thread
import time
import random
import smtplib

UMBRAL_CPU = 10
UMBRAL_MEMORIA = 60

MENSAJES_CPU = [
    "Uso elevado de CPU. Cierre algunas aplicaciones.",
    "CPU trabajando duro. Considere cerrar programas innecesarios.",
    "La CPU está ocupada. Verifique las aplicaciones en ejecución."
]

MENSAJES_MEMORIA = [
    "Uso elevado de memoria. Cierre algunas aplicaciones.",
    "Memoria en uso. Considere liberar espacio cerrando programas.",
    "La memoria está llegando al límite. Verifique las aplicaciones en ejecución."
]

class MonitoreoSistemaApp:

    def enviar_correo_gmail(self,asunto, cuerpo, destinatario):
        gmail_user = 'sotoj9268@gmail.com'
        gmail_password = 'irph qaob vmbx dupw'

        asunto = f'Subject: {asunto}'

        mensaje = f'{asunto}\n\n{cuerpo}'

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        try:
            server.login(gmail_user, gmail_password)

            server.sendmail(gmail_user, destinatario, mensaje)

            print(f'Correo enviado a {destinatario} con éxito.')

        except smtplib.SMTPAuthenticationError as e:
            print(f'Error de autenticación: {e}')

        except Exception as e:
            print(f'Error al enviar el correo: {e}')

        finally:
            server.quit()        

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Monitoreo de Sistema")

        self.etiqueta_cpu = tk.Label(self.ventana, text="", padx=20, pady=20)
        self.etiqueta_cpu.pack()

        self.etiqueta_memoria = tk.Label(self.ventana, text="", padx=20, pady=20)
        self.etiqueta_memoria.pack()

        boton_cerrar = tk.Button(self.ventana, text="Cerrar", command=self.ventana.destroy)
        boton_cerrar.pack()

    def monitorear_rendimiento(self):
        while True:
            uso_cpu = psutil.cpu_percent()
            uso_memoria = psutil.virtual_memory().percent

            if uso_cpu > UMBRAL_CPU:
                mensaje_cpu = f"Uso elevado de CPU: {uso_cpu}%\n{random.choice(MENSAJES_CPU)}"
                self.etiqueta_cpu.config(text=mensaje_cpu)

            time.sleep(5)

            if uso_memoria > UMBRAL_MEMORIA:
                mensaje_memoria = f"Uso elevado de Memoria: {uso_memoria}%\n{random.choice(MENSAJES_MEMORIA)}"
                self.etiqueta_memoria.config(text=mensaje_memoria)

            time.sleep(5)

            if uso_cpu > UMBRAL_CPU or uso_memoria > UMBRAL_MEMORIA:
                self.enviar_correo_gmail('Rendimiento excesivo', 'Cuerpo del mensaje', 'trigger@applet.ifttt.com')

if __name__ == "__main__":
    ventana = tk.Tk()

    app = MonitoreoSistemaApp(ventana)

    hilo_rendimiento = Thread(target=app.monitorear_rendimiento, daemon=True)
   
    hilo_rendimiento.start()

    ventana.mainloop()

    

