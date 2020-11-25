from sense_hat import SenseHat
from math import sqrt
import time
from time import sleep
Mysleep = 0.2
Realfall=0
Falsefall=0
norespond=0
acc=0
attente = 0
def fallClear():
	global Mysleep
	global attente
	global norepond
	global acc
	sense.clear()
	Mysleep=0.2
	acc = 0
	norespond=0
	attente = 0
def realfall():
	global attente
	global Realfall
	global acc
	if attente == 1:
		acc = 1
		attente = 0
		Realfall=1
		print("Vrai chute")
		sense.clear()
		#envoyer mail et tout remettre a 0
def falsefall():
	global attente
	global Falsefall
	global acc
	if attente == 1:
		acc = 1
		attente = 0
		falsefall=1
		print("Fausse alerte")
		sense.clear()

sense = SenseHat()
freefall=0
sense.stick.direction_middle=fallClear
sense.stick.direction_up=realfall
sense.stick.direction_down=falsefall

while True:
	sleep(Mysleep)
	acceleration = sense.get_accelerometer_raw()
	x = acceleration['x']*9.81
	y = acceleration['y']*9.81
	z = acceleration['z']*9.81
	a = sqrt(x*x + y*y + z*z)
	print(a)
	if a < 1:
		min = a
        	sense.clear(255,0,0)
		freefall=1
		Mysleep=0
	else:
		if freefall==1:
			if((a-min>12)):
				print("Il semblerait que vous etes tombe")
				print(a-min)
				attente = 1
				curr=time.time()
				sleep(5)
				if acc == 0:
					norespond = 1 #Chute sans reponse, envoyer mail et tout remettre a 0
					freefall = 0
			else:
				sense.clear()
				Mysleep=0.2
			freefall=0
			Mysleep=0.2
