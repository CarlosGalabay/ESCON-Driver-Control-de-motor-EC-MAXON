import tkinter as tk
from tkinter import Label, Entry, Button, StringVar
import serial
import threading
import time

class MotorControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Control de Motor")

        self.angle_var = StringVar()
        self.angle_label = Label(master, text="Ángulo Actual:")
        self.angle_label.grid(row=0, column=0)
        self.angle_entry = Entry(master, textvariable=self.angle_var, state='readonly')
        self.angle_entry.grid(row=0, column=1)

        self.kp_var = StringVar()
        self.kp_label = Label(master, text="Kp:")
        self.kp_label.grid(row=1, column=0)
        self.kp_entry = Entry(master, textvariable=self.kp_var)
        self.kp_entry.grid(row=1, column=1)

        self.kd_var = StringVar()
        self.kd_label = Label(master, text="Kd:")
        self.kd_label.grid(row=2, column=0)
        self.kd_entry = Entry(master, textvariable=self.kd_var)
        self.kd_entry.grid(row=2, column=1)

        self.status_var = StringVar()
        self.status_label = Label(master, text="Habilitar Motor (status1):")
        self.status_label.grid(row=3, column=0)
        self.status_entry = Entry(master, textvariable=self.status_var)
        self.status_entry.grid(row=3, column=1)

        self.desired_angle_var = StringVar()
        self.desired_angle_label = Label(master, text="Ángulo Deseado:")
        self.desired_angle_label.grid(row=4, column=0)
        self.desired_angle_entry = Entry(master, textvariable=self.desired_angle_var)
        self.desired_angle_entry.grid(row=4, column=1)

        self.enviar_button = Button(master, text="Enviar Comando", command=self.enviar_comando)
        self.enviar_button.grid(row=5, column=0, columnspan=2)

        self.debug_mode_var = StringVar()
        self.debug_mode_var.set("0")
        self.debug_mode_button = Button(master, text="Activar Modo Debug", command=self.toggle_debug_mode)
        self.debug_mode_button.grid(row=6, column=0, columnspan=2)

        # Estado inicial del modo debug
        self.debug_mode = False

        # Iniciar hilo para la actualización de datos
        self.update_thread = threading.Thread(target=self.actualizar_datos_thread, daemon=True)
        self.update_thread.start()

    def enviar_comando(self):
        comando = f"a{self.desired_angle_var.get()} P{self.kp_var.get()} d{self.kd_var.get()} s{self.status_var.get()} m{int(self.debug_mode)}\n"
        ser.write(comando.encode())

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        self.debug_mode_var.set(str(int(self.debug_mode)))

    def actualizar_datos_thread(self):
        while True:
            try:
                # Intentar leer el ángulo actual desde Arduino
                ser.write(b'angle\n')
                angle = ser.readline().decode().strip()
                # Actualizar la variable en el hilo principal
                self.master.after(0, self.angle_var.set, angle)
            except serial.SerialTimeoutException:
                # Manejar el timeout, por ejemplo, imprimiendo un mensaje de error
                print("Timeout al intentar leer desde Arduino")
            time.sleep(0.5)  # Esperar 0.5 segundos antes de la próxima actualización

if __name__ == "__main__":
    ser = serial.Serial('COM4', 115200, timeout=1)  # Agregamos un timeout para manejar mejor la lectura
    time.sleep(2)  # Esperar a que se estabilice la conexión serial

    root = tk.Tk()
    app = MotorControlApp(root)
    root.mainloop()
