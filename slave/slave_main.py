import pygame
import random
import time
import json
from huskylib import HuskyLensLibrary
import msgpackrpc
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
import time

# setting for HUSKEY Lens, door-bell
door_bell = 7
GPIO.setup(door_bell, GPIO.IN, pull_up_down=GPIO.PUD_UP)
hl= HuskyLensLibrary("I2C","",address=0x32)
hl.algorthim("ALGORITHM_FACE_RECOGNITION")
time.sleep(2)
client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))
switch_toggle = False

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("/home/hz/Desktop/doorbell.MP3")

# name list for HUSKEY Lens
nameList = ['stranger', 'jongbok', 'sunu', 'inho', 'sangdo']
last_send = 0

while(True):
	# When someone tap the bell-switch!    
	if GPIO.input(door_bell) == GPIO.LOW:
		switch_toggle = True
	if (GPIO.input(door_bell) == GPIO.HIGH) & (switch_toggle == True):
		switch_toggle = False
		pygame.mixer.music.play()
		print("hello!\n")
		try:
			print("test")
			temp = hl.requestAll()[0]
			print("test2")
			if(type(temp) != int):
				print("test3")
				idNum = temp.__dict__['ID']
				print("test4")
				idNum = 0 if idNum > 4 else idNum
				print(f"{nameList[idNum]}\n")
				if last_send == idNum:
					idNum += 5
				last_send = idNum
				client.call('sendtoCANE', idNum)
				print(idNum)
				time.sleep(2)
			time.sleep(1)
		except KeyboardInterrupt:
			print("\nQUITING")
			quit()
    # except TypeError:
    #     print("Please enter only a single letter")
		except IndexError:
			print("Command not found")
			try:
				idNum = 0
				if last_send == idNum:
					idNum += 5
				last_send = idNum
				client.call('sendtoCANE', idNum)
				print(idNum)
				time.sleep(3)
			except Exception:
				print("double error")
		except Exception as e:
        # General error -> just print it
			print(f"Error {e}")
