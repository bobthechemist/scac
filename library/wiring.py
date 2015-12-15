# Modified from MCP3008 tutorial by Limor Fried at Adafruit Industries

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Change as needed
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
YELLOW = 23
RED = 18

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
# set up the LED pins
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)


# Read SPI data from MCP3008 chip
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if((adcnum>7) or (adcnum <0)):
    return -1
  GPIO.output(cspin, True)
  GPIO.output(clockpin, False)
  GPIO.output(cspin, False)
  commandout = adcnum
  commandout |= 0x18
  commandout <<= 3
  for i in range(5):
    if (commandout & 0x80):
      GPIO.output(mosipin, True)
    else:
      GPIO.output(mosipin, False)
    commandout <<= 1
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
  adcout = 0
  for i in range(12):
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
    adcout <<= 1
    if (GPIO.input(misopin)):
      adcout |= 0x1
  GPIO.output(cspin, True)
  adcout >>= 1
  return adcout

def getData():
  return str(readadc(0,SPICLK,SPIMOSI,SPIMISO,SPICS))

def turnYellowOn():
  GPIO.output(YELLOW,True)
  return "Done"

def turnYellowOff():
  GPIO.output(YELLOW,False)
  return "Done"

def turnRedOn():
  GPIO.output(RED,True)
  return "Done"

def turnRedOff():
  GPIO.output(RED,False)
  return "Done"
