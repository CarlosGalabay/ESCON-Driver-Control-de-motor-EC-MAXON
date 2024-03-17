import serial
import time

# Especifica el puerto serial al que está conectado el Arduino (sustituye 'COMX' con el puerto correcto)
arduino_port = 'COM7'
arduino_baudrate = 9600

# Inicializa la conexión serial con el Arduino
arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
time.sleep(2)  # Espera a que se establezca la conexión

try:
    while True:
        # Envía comandos desde el teclado
        command = input("Ingrese comando (R1 para encender, R0 para apagar): ")
        arduino.write((command + '\n').encode())

        # Lee y muestra el valor del potenciómetro en A0
        potentiometer_value = arduino.readline().decode().strip()
        print(f"Valor del potenciómetro en A0: {potentiometer_value}")

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
finally:
    arduino.close()
