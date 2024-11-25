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

import matplotlib.pyplot as plt

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

print(f"impetanz:      {impetanz/1000:10.3f}kOhm")
print(f"Zeitkonstante: {tau*1000}ms")


#Datentyp List ist ein mutable - Objekt -> veränderbar - elemente hinzufügen, löschen, sortieren...
#Listen können Unterschiedliche Datentypen enthalten
#können auch andere listen enthalten
#nicht alle elemente müssen der gleiche datentyp sein

print("")
print("Datentyp list:")
print("=============")

myList = [1,2,3.1,"vier",[5.1,5.2,5.3],6,7j]

print(f"Element 0: {myList[0]}") #gibt das erste element aus
print(f"letze Element: {myList[-1]}")
print(f"erste Element aus 5. Element: {myList[4][0]}")
print(f"1.-3. Element: {myList[0:2+1]}") #gibt alle elemente von 1 bis ausschließlich 3+1 aus

print("")
print(f"von 3.Element bist schluss: {myList[2:]}")
print(f"{myList[:5:2]}") #jedes zweite element von stelle 0 bis ausschließlich 5
print(f"{myList[-2:]}") #vorletztes bis schluss
print(f"{myList[::2]}") #jedes zweite element

myList.append(1)
myList += [1]
print(myList[-1])
print(myList)

myList.insert(2,"Einfügen")
print(myList)

print("")
#entpacken von listen
a, b, c, = myList[:3]

print(f" a = {a}, b = {b}, c = {c}")


#Klasse RANGE
#==========================

#Rangers erzeugen eine Liste von Ganzzahlen
#Range() kann auf 3 verschiedene arten benutzt werden

#range(n) erzeugt Zahlen von 0 bis n-1
#range(start,end) erzeugt Zahlen von start, start+1, start+2 bis end
#range(start,end, stride) erzeugt Zahlen von start, start+stride, start+2*stride bis end



#Datentyp Tuples - imutable
#==========================

#wie liste die nicht verändert werden kann -> keine elemente wegnehmen oder dazugen oder ähnliches
print("")
print("Datentyp tuple:")
print("===============")

tup_numbers = (1,2,3,4) #statt [], (verwenden)

print(tup_numbers[2]) #zugriff troptzdem mit []
print(tup_numbers + (5,6)) #(1,2,3,4,5,6)
print(2*tup_numbers) #gibt tub_numbers 2 mal aus!! (1,2,3,4,1,2,3,4)
a, b, c, = tup_numbers[:3]

#viele Funktionen geben ihren als rückgabewert als tuple zurück
dm = divmod(11,3) #11/3 = 3 rest2 -> dm = (3,2)

print(dm)
print(f"11/3 = {dm[0]} rest: {dm[1]}")


#dictionaries
#=================

#dicts werden nicht über zahlen sondern beliebige schlüssel indiziert
#beim ertstellen werden schlüssel-wert-paare angeführt

print("")
print("Datentyp dict:")
print("=============")

person = {"vorname":"erik", "nachname":"prattner", "größe":1.82, "Klasse":"ahmba21"}

print(f"{person['vorname']} {person['nachname']} ist in der klasse {person['Klasse']}")
print(f"alle keys aus person: {person.keys}")

#SCHLEIFEN
#=========

#für y = x²
y = []
range_display = 100000

for x in range(range_display):
    #y.append(x**2)
    y += [x**2]

#y =[x**2 for x in range(5)]

plt.plot(range(range_display),y)
plt.ylabel("Y-Achse")
plt.xlabel("X-Achse")
plt.show()

y = []
x = 0
while x < S5:
    y += [x**2]
    x += 1
