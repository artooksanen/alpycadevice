import math
import time
import serial
import sys

# Serial Port and Speed Settings
serial_port = '/dev/ttyACM0'
#serial_port = '/dev/ttyUSB0'
baud_rate =9600
counter=0

def getxcounter():
  ser.write('?x\n'.encode())
  data = ser.read_until(b'\n').decode()
#  print("data:",data[:-1])
  if data.startswith("x="):
    x=data[:-1].split('=')[1].strip()

#    print(" x=",x)
#    ascii_values = [ord(char) for char in x]
#    print(f"The ASCII values for the string '{x}' are {ascii_values}")

    try:
      global counter
      counter=int(x)
    except ValueError:
      print("value error:",x)
#    print("getcounter_de: de_counter:",de_counter)
  return counter


def getycounter():
  ser.write('?y\n'.encode())
  data = ser.read_until(b'\n').decode()
#  print("data:",data[:-1])
  if data.startswith("y="):
    x=data[:-1].split('=')[1].strip()

#    print(" x=",x)
#    ascii_values = [ord(char) for char in x]
#    print(f"The ASCII values for the string '{x}' are {ascii_values}")

    try:
      global counter
      counter=int(x)
    except ValueError:
      print("value error:",x)
#    print("getcounter_de: de_counter:",de_counter)
  return counter





def connect():
   global ser,connection
# Serial Port Initialization
   ser = serial.Serial(serial_port, baud_rate,timeout=1)
   print("connect")

def disconnect():
   global connection
   # Serial Port Initialization
   print("disconnect")
   ser.close()

if __name__ == "__main__":

    connect()


    while True:
#      ser.write('xn=0\n'.encode())
#      ser.write('yn=2\n'.encode())
#      ser.write('xs=0\n'.encode())
#      ser.write('ys=1\n'.encode())
      x=getxcounter()
      y=getycounter()
      print("xcounter:",x,"ycounter:",y)
      time.sleep(1)


    disconnect()


