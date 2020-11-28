from sense_hat import SenseHat
from math import sqrt
import time
from time import sleep
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


msg = MIMEMultipart()
msg['From'] = 'info704projet1@gmail.com'
msg['To'] = 'dylan.baptiste@etudiant.univ-reims.fr'
msg['Subject'] = 'Le sujet de mon mail' 
message = 'Bonjour !'
msg.attach(MIMEText(message))
mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
mailserver.login('info704projet1@gmail.com', 'info0704')
mailserver.sendmail('info704projet1@gmail.com', 'dylan.baptiste@etudiant.univ-reims.fr', msg.as_string())
mailserver.quit()

DEFAULT_SLEEP_TIME = 0.2

sleep_time = DEFAULT_SLEEP_TIME

Realfall = 0
Falsefall = 0
norespond = 0
acc = 0
attente = False

sample_size = 100
time_sample = [1 for i in range(0, sample_size)]
sample = [1 for i in range(0, sample_size)]
saved_sample = []
saved_time_sample = []

def fallClear():
	global sleep_time
	global attente
	global norepond
	global acc
	sense.clear()
	sleep_time = DEFAULT_SLEEP_TIME
	acc = 0
	norespond = 0
	attente = False

def realfall():
	global attente
	global Realfall
	global acc
	if attente == True:
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
	if attente == True:
		acc = 1
		attente = False
		falsefall = 1
		print("Fausse alerte")
		sense.clear()

sense = SenseHat()
freefall = 0
sense.stick.direction_middle=fallClear
sense.stick.direction_up=realfall
sense.stick.direction_down=falsefall

last_time = time.time()

while True:
	sleep(sleep_time)
	
	acceleration = sense.get_accelerometer_raw()
	
	x = acceleration['x']*9.81
	y = acceleration['y']*9.81
	z = acceleration['z']*9.81
	global_acceleration = sqrt(x*x + y*y + z*z)
	
	sample.append(global_acceleration)
	sample.pop(0)

	current_time = time.time() - last_time 
	time_sample.append(current_time)
	time_sample.pop(0)

	print(current_time, global_acceleration)
	
	if global_acceleration < 1:
		min = global_acceleration
		sense.clear(255, 0, 0)
		freefall = 1
		sleep_time = 0
	else:
		if freefall == 1:
			impact_force = global_acceleration - min #todo chercher le max dans le sample
			if(impact_force > 10):
				# Impact
				freefall = 0
				print("Impact de {}g apres chute libre".format(impact_force/9.81))
				
				impact_time = time.time()
				attente = True
				sleep_time = DEFAULT_SLEEP_TIME
			else:				
				sense.clear()
				sleep_time = DEFAULT_SLEEP_TIME

			freefall = 0
		else:
			if(attente == True):
				print("time", time.time() - impact_time )
				if(time.time() - impact_time > 5):
					if acc == 0:
						attente = False
						norespond = 1 #Chute sans reponse, envoyer mail et tout remettre a 0
				if(time.time() - impact_time > 2):
					fig = plt.figure(figsize=(10,5))
					plt.plot(time_sample, sample, label="g")
					plt.xlabel('temps') 
					plt.ylabel('g') 
					plt.title('Chute')
					plt.legend()
					fig.savefig('chute.jpg', bbox_inches='tight', dpi=150)
