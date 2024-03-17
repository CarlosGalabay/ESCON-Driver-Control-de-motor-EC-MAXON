import pyfirmata2
import time

# Creates a new board
PORT = pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT)
print("Estableciendo conexión ...")

# Variables
HallSensorU_pin = board.get_pin('d:19:i')
HallSensorV_pin = board.get_pin('d:20:i')
HallSensorW_pin = board.get_pin('d:21:i')

CW = 1
CCW = -1

en = 12
sped = 7

motor_steps = 72
reduction = 1

Kp = 0.7
Kd = 1.0

step_to_deg = (motor_steps * reduction) / 360

direct = 1
pulseCount = 0

desired_angle = 0.0

angle = 0.0

desired_step = 0.0

error = 0
prev_error = 0

HSU_Val = False
HSV_Val = False
HSW_Val = False

debug_mode = 0
status1 = 0

# Callbacks
def HallSensorW():
  HSW_Val = HallSensorW_pin.read()
  HSV_Val = HallSensorV_pin.read()
  direct = CW if (HSW_Val == HSV_Val) else CCW
  pulseCount = pulseCount + (1 * direct)

def HallSensorV():
  HSV_Val = HallSensorV_pin.read()
  HSU_Val = HallSensorU_pin.read()
  direct = CW if (HSV_Val == HSU_Val) else CCW
  pulseCount = pulseCount + (1 * direct)

def HallSensorU():
  HSU_Val = HallSensorU_pin.read()
  HSW_Val = HallSensorW_pin.read()
  direct = CW if (HSU_Val == HSW_Val) else CCW
  pulseCount = pulseCount + (1 * direct)

  