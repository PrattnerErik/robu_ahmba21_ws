#
'''
lol
'''

#enter python interpreter:
#python3
#extit()

import math #importiert ganze lib
from math import pi # importiert zahl pi
from math import pi as M_pi # importier pi als M_pi

import matplotlib.pyplot as pit

# dynamische typisierung:
# variable kann verschiedene Datentypen haben

titel = "datentypen"
vorname = "erik"
nachname = "prattner"
name = vorname + " " + nachname
klassenvorstand = True
groesse = 1.83
schuhgroesse = 46
impetanz = 420 + 69j #komplexe zahl als datentyp

print("Ausgabe von Unterschiedlichen", 3*(" " +titel))
print(f"mein name ist {name}")
print(klassenvorstand, type(klassenvorstand))
print(impetanz, type(impetanz))

print("impetanz berechnen")
print("==================")

resistor = 1000
capacitor = 1e-6
frequency = 50.

impetanz = complex(resistor, 1/(2*pi*capacitor*frequency))

tau = resistor * capacitor

print(f"impetanz: {impetanz/1000:10.3f}kOhm")
print(f"Zeitkonstante: {tau*1000}ms")