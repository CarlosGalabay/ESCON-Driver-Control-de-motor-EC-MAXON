import tkinter as tk
from pyfirmata2 import Arduino
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import sys
import numpy as np

class ArduinoInterface:
    def __init__(self, arduino_port='COM7'):
        self.board = Arduino(arduino_port)
        self.board.samplingOn()
        self.analog_pin = self.board.get_pin('a:0:i')
        self.digital_pin = self.board.get_pin('d:13:o')
        self.valor = 0.0

        self.root = tk.Tk()
        self.root.title("Arduino Interface")

        # Etiqueta para mostrar el valor del potenciómetro
        self.label = tk.Label(self.root, text="Valor del Potenciómetro:")
        self.label.pack()

        # Etiqueta dinámica para mostrar el valor en tiempo real
        self.value_label = tk.Label(self.root, text="0.0")
        self.value_label.pack()

        # Inicializa la figura para el gráfico
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_ylim(0, 1)

        # Configura un manejador de devolución de llamada para el pin analógico
        self.analog_pin.register_callback(self.analog_callback)

        # Añade el lienzo de la figura a la interfaz gráfica
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Hilo para actualizar la interfaz gráfica en segundo plano
        self.update_thread = threading.Thread(target=self.update_gui)
        self.running = True
        self.update_thread.start()

    def analog_callback(self, data):
        # Manejador de devolución de llamada para el pin analógico
        self.valor = data

    def update_gui(self):
        x_data = np.arange(100)  # Inicializa con 100 puntos
        y_data = np.zeros(100)   # Inicializa con 100 ceros
        try:
            while self.running:
                # Actualiza la etiqueta con el valor actual
                self.value_label.config(text=f"{self.valor:.2f}")

                # Actualiza el gráfico en tiempo real
                y_data = np.roll(y_data, -1)  # Desplaza los datos hacia la izquierda
                y_data[-1] = self.valor        # Añade el nuevo dato al final

                # Actualiza la posición de la línea de la gráfica
                self.line.set_data(x_data, y_data)

                # Ajusta el límite del eje x según el tamaño de los datos
                xlim_min = 0
                xlim_max = len(x_data) - 1
                self.ax.set_xlim(xlim_min, xlim_max)

                # Actualiza la interfaz cada 100 milisegundos (ajusta según sea necesario)
                self.canvas.draw()
                self.root.update()
                time.sleep(0.1)
        except Exception:
            sys.exit()
        finally:
            print("Fin del código!!!")

    def turn_on_led(self):
        # Enciende el LED
        self.digital_pin.write(1)

    def turn_off_led(self):
        # Apaga el LED
        self.digital_pin.write(0)

    def run(self):
        # Inicia el bucle principal de la interfaz gráfica
        self.root.mainloop()

    def stop_update_thread(self):
        # Detiene el hilo de actualización de la GUI
        self.running = False
        self.update_thread.join()

# Crea una instancia de la interfaz y ejecútala
interface = ArduinoInterface()
interface.run()
