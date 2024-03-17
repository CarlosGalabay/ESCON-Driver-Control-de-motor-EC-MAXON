from pyfirmata2 import Arduino, util
import time

# Conecta con el Arduino (especifica el puerto correcto)
arduino_port = 'COM4'
board = Arduino(arduino_port)

valor = 0
pin = board.get_pin('d:12:i')
def pinCallback(self):
        print(pin.read())
        if pin.read() == 0:
            print("Hola")




# Setup the digital pin with pullup resistor: "u"
digital_0 = board.get_pin('d:6:i')

# points to the callback
digital_0.register_callback(pinCallback)

# default sampling interval of 19ms
board.samplingOn()

# Espera a que se establezca la conexión
#time.sleep(2)
print("START!")
valor = 0
try:
    while True:
        pass


             

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
finally:
    board.exit()
