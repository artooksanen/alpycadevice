from datetime import datetime, timezone
import time
import hor
import arduino
import math

epookki0=epookki1=2000.0
t=0.0
ta=0.0
ta0=0
ra=0.0
de=0.0
ats=0.0
kor=0.0
target_ra=0.0
target_de=0.0
ra_slewing=False
de_slewing=False
#2.086 0.2317
counterstep_ra=(1.0)/3600.0    # tuntia
counterstep_de=(10.0)/3600.0       # astetta
ra0=0
de0=0

def connect():
  global counter_ra0,counter_de0
  print("rade.connect(): arduino.connect() ->")
  arduino.connect()
  print("rade.connect(): arduino.connect() <-")
  print("rade.connect(): arduino.get_counters) ->")
  counter_ra0=0 #arduino.getcounter_ra()
  counter_de0=0 #arduino.getcounter_de()
  print("rade.connect(): arduino.get_counters <-")

def disconnect():
  print("rade.disconnect()")
  arduino.disconnect()

def connected():
  return arduino.connected()

def utcdate():
  return datetime.now().isoformat() 

def eponch(r,d,e1,e2):
  return (r,d)

def update_time():
   global t,ta
   ut=datetime.utcnow()
   lt=datetime.now()
   y=ut.year
   m=ut.month
   d=ut.day
   hh=ut.hour
   mm=ut.minute
   ss=ut.second
   t=hor.tojd(y,m,d,hh,mm,ss)
   ta=hor.taika(t)

def get_siderealtime():
  update_time()
  return(ta)

def update_coord(i):
  global t,ra,de,ats,kor
  (ra,de)=get_coord()                        # luetaan koordinaatit
  (ra1,de1)=epoch(ra,de,epookki0,epookki1)
  (ats,kor)=hor.atkor(ra,de,t)

def get_azimuth():
  update_time()
  (ats,kor)=hor.atkor(ra,de,t)
  return ats

def get_altitude():
  update_time()
  (ats,kor)=hor.atkor(ra,de,t)
  return kor

def get_ra():
  global ra_slewing,ra,ra0,ta,counter_ra0,ta0
#rektaskension ajonopeudet
  rn1=1.0/3600.0 # hidas nopeus
  rn2=60.0/3600.0 # keskinopeus
  rn3=600.0/3600.0 #nopea nopeus
  update_time()
#  print("ra counter=",arduino.getcounter_ra(),"counter0=",counter_ra0,"ta=",ta)
  ra=ra0-(arduino.getcounter_ra()-counter_ra0)*counterstep_ra+(ta-ta0)
  if ra<0:
    ra=ra+24
  if ra>24:
    ra=ra-24
  if ra_slewing:
    delta=target_ra-ra
    if delta>12:
      delta=delta-24
    if delta<-12:
      delta=delta+24
    if delta<0:
     suunta=1
    else:
     suunta=-1
    nopeus=0
    if abs(delta)>rn1:
      nopeus=1
    if abs(delta)>rn2:
      nopeus=2
    if abs(delta)>rn3:
      nopeus=3
    if abs(delta)>12.0:
      suunta=-suunta
    if nopeus==0:
      ra_slewing=False
      suunta=0
    arduino.setspeed_ra(suunta,nopeus)
  return ra

def get_de():
  global de_slewing,de,de0
 # deklinaation ajonopeudet
  dn1=1.0/60.0 # hidas nopeus
  dn2=10.0/60.0 # keskinopeus
  dn3=60.0/60.0 # suuri nopeus
  de=de0+(arduino.getcounter_de()-counter_de0)*counterstep_de
  if de_slewing:
    delta=target_de-de
    if delta<0:
     suunta=-1
    else:
     suunta=1
    nopeus=0
    if abs(delta)>dn1:
      nopeus=1
    if abs(delta)>dn2:
      nopeus=2
    if abs(delta)>dn3:
      nopeus=3
    if nopeus==0:
      de_slewing=False
      suunta=0
    arduino.setspeed_de(suunta,nopeus)
  return de

def set_ra(r):
  global ra,ra0,counter_ra0,ta0
  counter_ra0=arduino.getcounter_ra()
  ra0=ra=r
  update_time()
  ta0=ta
#  print("set ra=",ra)

def set_de(d):
  global de,de0,counter_de0
  counter_de0=arduino.getcounter_de()
  de0=de=d
#  print("set de=",de)

def slew(r,d):
  global target_ra,target_de,ra_slewing,de_slewing
  target_ra=r
  target_de=d
  ra_slewing=True
  de_slewing=True

def abortslew():
  global ra_slewing,de_slewing
  ra_slewing=False
  de_slewing=False
  arduino.setspeed_ra(0,0)
  arduino.setspeed_de(0,0)
 
def is_slewing():
  return ra_slewing or de_slewing


