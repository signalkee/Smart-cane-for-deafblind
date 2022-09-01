import random
import msgpackrpc
import time
time.sleep(30)
client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))
import json
from huskylib import HuskyLensLibrary
hl= HuskyLensLibrary("I2C","",address=0x32)

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

vib = 18
GPIO.setup(vib, GPIO.OUT)
GPIO.output(vib, GPIO.LOW)

toggle_up = False
toggle_down = False
toggle_left = False
toggle_right = False
button_up = 10       # IoT -> rice(UP), airconditioner(LEFT), washing machine(RIGHT)
button_down = 29     # tutorial
button_left = 26     # money
button_right = 13    # Traffic light
GPIO.setup(button_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SwitchMode = 0
IoTMode = 0

doorbell = 0
last_doorbel = 0
nameList = ["stranger", "jongbok", "sunu", "inho", "sangdo"]
GPIO.output(vib, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(vib, GPIO.LOW)
while True: # main loop
    
    # door bell
	doorbell = client.call('readsend', 1)
	if doorbell != last_doorbel:
		doorbell = doorbell % 5
		print(f"{nameList[doorbell]} arrive!")
		GPIO.output(vib, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(vib, GPIO.LOW)
		last_doorbell = doorbell
    
    # BUTTON UP
	if GPIO.input(button_up) == GPIO.LOW:
		toggle_up = True
	if (GPIO.input(button_up) == GPIO.HIGH) & (toggle_up == True):
		toggle_up = False
		GPIO.output(vib, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(vib, GPIO.LOW)
		print("button_up was pushed!")
		
		SwitchMode = 0
		
		# if got into IoTMode, cook rice! 
		if(IoTMode == 1):
			print(f"activate rice cooker!")
			client.call('send', 5)  
			time.sleep(3)
			# return to default setting(non-IoTMode)
			IoTMode = 0
			
		# get into IoTMode
		else:
			IoTMode = 1

	# BUTTON DOWN
	if GPIO.input(button_down) == GPIO.LOW:
		toggle_down = True
	if (GPIO.input(button_down) == GPIO.HIGH) & (toggle_down == True):
		toggle_down = False
		GPIO.output(vib, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(vib, GPIO.LOW)
		print("button_down was pushed!")
		
		# TUTORIAL, IOT TUTORIAL
		
		# if got into IoTMode, give IoTMode tutorial!
		if(IoTMode == 1):
			print(f"IoTMode tutorial!")
			'''
			DO SOMETHING
			'''
			# return to default setting(non-IoTMode)
			IoTMode = 0
			SwitchMode = 0
			
		# default tutorial
		else:
			print(f"baseMode tutorial!")
			SwitchMode = 0
  

	# BUTTON LEFT
	if GPIO.input(button_left) == GPIO.LOW:
		toggle_left = True
	if (GPIO.input(button_left) == GPIO.HIGH) & (toggle_left == True):
		toggle_left = False
		GPIO.output(vib, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(vib, GPIO.LOW)
		print("button_left was pushed!")
		
		# MONEY CLASSIFICATION & AIRCONDITIONER
		
		# if got into IoTMode, airconditioner!
		if(IoTMode == 1):
			print(f"airconditioner!")
			client.call('send', 6)  
			time.sleep(3)
			# return to default setting(non-IoTMode)
			IoTMode = 0
			
		else:
			if SwitchMode == 3:
				SwitchMode = 0
			else:
				SwitchMode = 3
				hl.algorthim("ALGORITHM_FACE_RECOGNITION")
				time.sleep(1)

# money classification - face recognition
	if(SwitchMode == 3):
		try:
			#hl.algorthim("ALGORITHM_FACE_RECOGNITION")
			#time.sleep(0.3)
			if(type(hl.requestAll()[0]) != int):
				money_num = hl.requestAll()[0].__dict__['ID']
				if(money_num == 1):
					print(f"1000won")
					time.sleep(1)
				elif(money_num == 2):
					print(f"5000won")
					time.sleep(1)
				elif(money_num == 3):
					print(f"10000won")
					time.sleep(1)
				elif(money_num > 3):
					print(f"50000won")
					time.sleep(1)
		except KeyboardInterrupt:
			print("\nQUITING")
			quit()
		except IndexError:
			print(f"cc")
		except Exception as e:
			print(f"Error {e}")

	# BUTTON RIGHT
	if GPIO.input(button_right) == GPIO.LOW:
		toggle_right = True
	if (GPIO.input(button_right) == GPIO.HIGH) & (toggle_right == True):
		toggle_right = False
		GPIO.output(vib, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(vib, GPIO.LOW)
		print("button_right was pushed!")
		
		# TRAFFIC LIGHT & WASHING MACHINE
		
		# if got into IoTMode, washing machine!
		if(IoTMode == 1):
			print(f"washing machine!")
			client.call('send', 13)  
			time.sleep(3)
			# return to default setting(non-IoTMode)
			IoTMode = 0
		else:
			if SwitchMode == 4:
				SwitchMode = 0
			else:
				SwitchMode = 4

# Traffic light - object classification & color recognition
	if(SwitchMode == 4):
		try:
			hl.algorthim("ALGORITHM_OBJECT_CLASSIFICATION")
			time.sleep(0.3)
			if(type(hl.requestAll()[0]) != int):
				temp = hl.requestAll()[0].__dict__['ID']
			if(temp == True):
				hl.algorthim("ALGORITHM_COLOR_RECOGNITION")
				time.sleep(0.3)
				if(type(hl.requestAll()[0]) != int):
					trfc_light = hl.requestAll()[0].__dict__['ID']
					if(trfc_light > 3):
						print(f"stopppppp")
						time.sleep(1)
					elif(trfc_light >= 1) & (trfc_light <= 3):
						print(f"goooooooo")
						time.sleep(1)
		except KeyboardInterrupt:
			print("\nQUITING")
			quit()
		except IndexError:
			print(f"cc")
		except Exception as e:
			print(f"Error {e}")  
