import math
import time

ra_nopeus=0
ra_suunta=0
ra_laskuri=0
ra_counter=0
ra_lasttime=0.0

de_nopeus=0
de_suunta=0
de_laskuri=0
de_counter=0
de_lasttime=0.0

def setspeed_ra(suunta,nopeus):
  global ra_nopeus, ra_suunta, ra_lasttime
  ra_nopeus=nopeus
  ra_suunta=suunta
#  ra_lasttime=time.time()
#  print("setspeed_ra:",suunta,nopeus)

def setspeed_de(suunta,nopeus):
  global de_nopeus, de_suunta,de_lasttime
  de_nopeus=nopeus
  de_suunta=suunta
#  de_lasttime=time.time()
#  print("setspeed_de:",suunta,nopeus)

def getcounter_ra():
  global ra_counter,ra_lasttime
  now=time.time()
  if ra_lasttime!=0.0:
#   c=(ft1.time+ft1.millitm/1000.0-fte.time-fte.millitm/1000.0)*(1.002737/rapulse);
    ra_counter=ra_counter+20.0*math.pow(10.0,ra_nopeus-1)*ra_suunta*(now-ra_lasttime)
  ra_lasttime=now
  return ra_counter

def getcounter_de():
  global de_counter,de_lasttime
  now=time.time()
  if de_lasttime!=0.0:
    de_counter=de_counter+10.0*math.pow(10.0,de_nopeus-1)*de_suunta*(now-de_lasttime)
  de_lasttime=now
  return de_counter
