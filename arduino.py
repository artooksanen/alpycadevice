import math
import time
import serial
import sys

# Serial Port and Speed Settings

#oksanen@raspberrypi:~ $ ls /dev/serial/by-path/ -l
#lrwxrwxrwx 1 root root 13 Jun 28 11:17 platform-3f980000.usb-usb-0:1.2:1.0 -> ../../ttyACM0
#lrwxrwxrwx 1 root root 13 Jun 28 11:17 platform-3f980000.usb-usb-0:1.4:1.0 -> ../../ttyACM1

#oksanen@raspberrypi:~/AlpycaDevice/device $ ls /dev/serial/by-path/ -l
#lrwxrwxrwx 1 root root 13 Jul 16 17:27 platform-3f980000.usb-usb-0:1.1.2:1.0 -> ../../ttyACM1
#lrwxrwxrwx 1 root root 13 Jul 16 17:27 platform-3f980000.usb-usb-0:1.3:1.0 -> ../../ttyACM0


serial_port = '/dev/ttyACM1'
baud_rate = 9600
connection=False

ra_nopeus=0
ra_suunta=0
ra_laskuri=0
ra_counter=0
ra_lasttime=0.0

de_nopeus=0
de_suunta=0
de_laskuri=0
de_counter=0



def setspeed_ra(suunta,nopeus):
  print("setspeed_ra:",suunta,nopeus)
  if(nopeus==0):
    ser.write("xn=0\n".encode())
  if(nopeus==1):
    ser.write("xn=1\n".encode())
  if(nopeus==2):
    ser.write("xn=2\n".encode())
  if(nopeus==3):
    ser.write("xn=3\n".encode())

  if(suunta==1):
    ser.write("xs=1\n".encode())
  if(suunta==0):
    ser.write("xs=0\n".encode())
  if(suunta==-1):
    ser.write("xs=-1\n".encode())

def setspeed_de(suunta,nopeus):
  print("setspeed_de:",suunta,nopeus)
  if(nopeus==0):
    ser.write("yn=0\n".encode())
  if(nopeus==1):
    ser.write("yn=1\n".encode())
  if(nopeus==2):
    ser.write("yn=2\n".encode())
  if(nopeus==3):
    ser.write("yn=3\n".encode())

  if(suunta==1):
    ser.write("ys=1\n".encode())
  if(suunta==0):
    ser.write("ys=0\n".encode())
  if(suunta==-1):
    ser.write("ys=-1\n".encode())

def getcounter_ra():
  global ra_counter,ra_lasttime
#  print("getcounter_ra():")
  ser.write('?x\n'.encode())
  data = ser.read_until(b'\n').decode()
#  print("getcounter_ra data:",data[:-1])
  if data.startswith("x="):
    x=data[:-1].split('=')[1].strip()

#    print("getcounter_ra: x=",x)

#    ascii_values = [ord(char) for char in x]
#    print(f"The ASCII values for the string '{x}' are {ascii_values}")

    try:
      global ra_counter
      ra_counter=int(x)
    except ValueError:
      print("value error:",x)
#    print("getcounter_ra: ra_counter:",ra_counter)
  return ra_counter

def getcounter_de():
  global de_counter,de_lasttime
#  print("getcounter_de():")
  ser.write('?y\n'.encode())
  data = ser.read_until(b'\n').decode()
#  print("getcounter_de data:",data[:-1])
  if data.startswith("y="):
    x=data[:-1].split('=')[1].strip()

#    print("getcounter_de: x=",x)

#    ascii_values = [ord(char) for char in x]
#    print(f"The ASCII values for the string '{x}' are {ascii_values}")

    try:
      global de_counter
      de_counter=int(x)
    except ValueError:
      print("value error:",x)
#    print("getcounter_de: de_counter:",de_counter)
  return de_counter

def connected():
   global ser
# Serial Port Initialization
#   ser = serial.Serial(serial_port, baud_rate)
#   print("connect")
   return connection

def connect():
   global ser,connection
# Serial Port Initialization
   print("connect in")
   ser = serial.Serial(serial_port, baud_rate, timeout = 1)
   connection=True
   ser.write('xn=0\n'.encode())
   ser.write('yn=0\n'.encode())
   ser.write('xs=0\n'.encode())
   ser.write('ys=0\n'.encode())
   print("connect out")

def disconnect():
   global connection
   # Serial Port Initialization
   print("disconnect")
   if connection:
     ser.close()
   connection=False

if __name__ == "__main__":

    connect()

    c=getcounter_ra()
    print("initial ra counter:",c)
    c=getcounter_de()
    print("initial de counter:",c)

    c=getcounter_ra()
    print("ra counter:",c)
    c=getcounter_de()
    print("de counter:",c)

#    disconnect()

#    exit()

    print("slewing 10 seconds - speed 1")
    setspeed_ra(1,1)
    setspeed_de(1,1)
    time.sleep(10)

    c=getcounter_ra()
    print("ra counter:",c)
    c=getcounter_de()
    print("de counter:",c)

    print("slewing 10 seconds - speed 2")
    setspeed_ra(1,2)
    setspeed_de(1,2)
    time.sleep(10)

    c=getcounter_ra()
    print("ra counter:",c)
    c=getcounter_de()
    print("de counter:",c)

    print("slewing 10 seconds - speed 3")
    setspeed_ra(1,3)
    setspeed_de(1,3)
    time.sleep(10)

    print("speed 0")

    setspeed_ra(0,0)
    setspeed_de(0,0)

    c=getcounter_ra()
    print("final ra counter:",c)

    c=getcounter_de()
    print("final de counter:",c)

    disconnect()


