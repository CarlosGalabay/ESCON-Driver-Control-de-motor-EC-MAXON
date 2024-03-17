import serial
import time

# Establecer la conexión serial con Arduino
ser = serial.Serial('COM5', 9600)  # Asegúrate de cambiar 'COM3' al puerto correcto de tu Arduino

# Esperar a que se estabilice la conexión serial
time.sleep(2)

print("CONEXIÓN EXITOSA!!!")

try:
    while True:
        # Leer el estado del botón desde Arduino
        button_state = ser.readline().decode().strip()

        # Imprimir el estado del botón
        print(f'Estado del botón: {button_state}')

        # Cambiar el estado del LED en función del estado del botón
        if button_state == '1':
            print('Encendiendo LED...')
            # Aquí puedes agregar tu lógica para controlar el LED encendiéndolo
        elif button_state == '0':
            print('Apagando LED...')
            # Aquí puedes agregar tu lógica para controlar el LED apagándolo

        # Esperar un momento antes de volver a leer el estado del botón
        time.sleep(0.1)

except KeyboardInterrupt:
    # Cerrar la conexión serial al finalizar
    ser.close()
