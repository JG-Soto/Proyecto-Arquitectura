import psutil
import smtplib
import tkinter as tk
from threading import Thread
import time
import random
import geocoder
from geopy.distance import geodesic

UMBRAL_CPU = 10
UMBRAL_MEMORIA = 10

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
        gmail_password = ' '

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

    def __init__(self, titulo, umbral, mensajes, mensaje_ventana, ventana_padre=None):
        self.ventana = tk.Toplevel(ventana_padre) if ventana_padre else tk.Tk()
        self.ventana.title(titulo)

        self.etiqueta = tk.Label(self.ventana, text="", padx=20, pady=20)
        self.etiqueta.pack()

        self.umbral = umbral
        self.mensajes = mensajes
        self.mensaje_ventana = mensaje_ventana

        self.ventana.withdraw()

        self.detener_ejecucion = False

    def mostrar_ventana(self, mensaje):
        self.etiqueta.config(text=mensaje)
        self.ventana.after(0, self.ventana.deiconify)

    def ocultar_ventana(self):
        self.ventana.withdraw()

    def monitorear_cpu_paginado(self):
        intervalo = 1
        while not self.detener_ejecucion:
            uso_previo = 0
            tiempo_inicio = time.time()
            while time.time() - tiempo_inicio < intervalo and not self.detener_ejecucion:
                uso = psutil.cpu_percent()
                if uso > self.umbral and uso != uso_previo:
                    mensaje = f"{self.mensaje_ventana}: {uso}%\n{random.choice(self.mensajes)}"
                    self.mostrar_ventana(mensaje)
                else:
                    self.ocultar_ventana()
                uso_previo = uso
                time.sleep(5)

    def monitorear_memoria_paginado(self):
        intervalo = 1
        while not self.detener_ejecucion:
            uso_previo = 0
            tiempo_inicio = time.time()
            while time.time() - tiempo_inicio < intervalo and not self.detener_ejecucion:
                uso = psutil.virtual_memory().percent
                if uso > self.umbral and uso != uso_previo:
                    mensaje = f"{self.mensaje_ventana}: {uso}%\n{random.choice(self.mensajes)}"
                    self.mostrar_ventana(mensaje)
                else:
                    self.ocultar_ventana()
                uso_previo = uso
                time.sleep(5)


    def obtener_coordenadas(self):
        ubicacion = geocoder.ip('me')

        if ubicacion.latlng:
            return ubicacion.latlng
        else:
            return None

    def dentro_del_radio(self, coordenadas1, coordenadas2, radio):
        distancia = geodesic(coordenadas1, coordenadas2).meters
        return distancia <= radio

    def ubicacion(self):
        lat_inicial = -00.1143
        lon_inicial = -78.4867
        coordenadas_anteriores = [lat_inicial, lon_inicial]

        radio_input = 0.5

        while not self.detener_ejecucion:
            try:
                time.sleep(60)
                coordenadas_actuales = self.obtener_coordenadas()

                if coordenadas_actuales is None:
                    print("No se pudieron obtener las coordenadas actuales. Verifica tu conexión a Internet.")
                    continue

                if not self.dentro_del_radio(coordenadas_anteriores, coordenadas_actuales, radio_input):
                    print(f"¡Cambio de ubicación detectado! Deteniendo el script.")
                    self.enviar_correo_gmail('Rendimiento excesivo', 'Cuerpo del mensaje', 'trigger@applet.ifttt.com')
                    self.detener_ejecucion = True
            except KeyboardInterrupt:
                print("Script detenido manualmente.")
                break

        self.ventana.quit()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    ventana_principal.withdraw()

    app_cpu = MonitoreoSistemaApp("Monitoreo de CPU", UMBRAL_CPU, MENSAJES_CPU, "Uso elevado de CPU", ventana_principal)
    app_memoria = MonitoreoSistemaApp("Monitoreo de Memoria", UMBRAL_MEMORIA, MENSAJES_MEMORIA, "Uso elevado de Memoria", ventana_principal)
    app_ubicacion = MonitoreoSistemaApp("Ubicacion", 0.5, "Ha salido del área establecida", None, None)

    hilo_cpu = Thread(target=app_cpu.monitorear_cpu_paginado, daemon=True)  # Cambio aquí
    hilo_memoria = Thread(target=app_memoria.monitorear_memoria_paginado, daemon=True)  # Cambio aquí
    hilo_ubicacion = Thread(target=app_ubicacion.ubicacion, daemon=True)
   
    hilo_cpu.start()
    hilo_memoria.start()
    hilo_ubicacion.start()

    ventana_principal.mainloop()