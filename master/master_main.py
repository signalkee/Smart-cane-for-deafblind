import random
import msgpackrpc
import time
import serial
# time.sleep(40)
try:
	client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))
except Exception as e:
	print('no server')
import json
from huskylib import HuskyLensLibrary
hl= HuskyLensLibrary("I2C","",address=0x32)
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# dot
dot_pad_sync = b'\xAA\x55'
dot_pad_20_len = b'\x00\x1A'
dot_pad_20_dest_id = b'\x00'
dot_pad_display_cmd = b'\x02\x00'
dot_pad_seq_num = b'\x80'
dot_pad_offset = b'\x00'
dot_pad_display_header = dot_pad_sync + dot_pad_20_len + dot_pad_20_dest_id + dot_pad_display_cmd + dot_pad_seq_num + dot_pad_offset
all_up_data = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
choinjong = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x25\x1F\x28\x3F'
JB = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x28\x3F\x18\x2D'
SW = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x3E\x0D'
IH = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1F\x1A\x25'
SD = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x36\x0A\x25'
DAEKI = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\x17\x08\x15'
RED = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x18\x02'
GREEN = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x25'
CHEON = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x3E'
OHCHEON = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x25\x30\x3E'
MANN = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x12'
OHMANN = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x25\x11\x12'
BOTPOT = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x03\x20\x25\x26'
AIRCON = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1D\x0E\x0B\x3E'
SETACKI = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x1D\x13\x01\x08\x15'
MENUAL = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x1E\x11\x3B'



all_down_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


dot_pad_check_sum_len = 1
dot_pad_check_sum_offset = 4


def get_check_sum(buf, len):
	check_sum = int.from_bytes(b'\xA5', byteorder='big')
	for i in range(0, len):
		check_sum = check_sum ^ buf[i]
	return check_sum.to_bytes(1, byteorder='big')

def write_dot(dotCode=all_down_data):
	write_data = dot_pad_display_header + dotCode
	check_sum = get_check_sum(write_data[dot_pad_check_sum_offset:], int.from_bytes(dot_pad_20_len, byteorder='big') - dot_pad_check_sum_len)
	ser.write(write_data + check_sum)



 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # check dev!!!
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.xonxoff = True
ser.rtscts = False
ser.dsrdtr = False
ser.write_timeout = 0

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
isServer = True

doorbell = 0
last_doorbell = 0
nameList = ["stranger", "jongbok", "sunu", "inho", "sangdo"]

GPIO.output(vib, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(vib, GPIO.LOW)
write_dot(all_down_data)
while True: # main loop
    # door bell
	try:
		doorbell = client.call('readsend', 1)
		print(doorbell)
	except Exception as e:
		try:
			client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))
		except Exception as e:
			print('no server')

	if doorbell != last_doorbell:
		last_doorbell = doorbell
		doorbell = doorbell % 5
		print(f"{nameList[doorbell]} arrive!")
		GPIO.output(vib, GPIO.HIGH)
		if doorbell == 0:
			write_dot(choinjong)
		elif doorbell== 1:
			write_dot(JB)
		elif doorbell== 2:
			write_dot(SW)
		elif doorbell== 3:
			write_dot(IH)
		elif doorbell== 4:
			write_dot(SD)
		time.sleep(2)
		GPIO.output(vib, GPIO.LOW)
		time.sleep(1)
		write_dot(all_down_data)
		write_dot()
    
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
			try:
				print(f"activate rice cooker!")
				client.call('send', 5)
				write_dot(BOTPOT)
				time.sleep(3)
				write_dot(all_down_data)
			except Exception as e:
				print('no server!')
				
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
			write_dot(MENUAL)
			time.sleep(3)
			write_dot(all_down_data)
			# return to default setting(non-IoTMode)
			IoTMode = 0
			SwitchMode = 0
			
		# default tutorial
		else:
			print(f"baseMode tutorial!")
			SwitchMode = 0
			write_dot(MENUAL)
			time.sleep(3)
			write_dot(all_down_data)
  

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
			try:
				print("airconditioner!")
				client.call('send', 6)
				write_dot(AIRCON)
				time.sleep(3)
				write_dot(all_down_data)
			except Exception as e:
				print('no server!')
			# return to default setting(non-IoTMode)
			IoTMode = 0
			
		else:
			if SwitchMode == 3:
				SwitchMode = 0
			else:
				SwitchMode = 3
				hl.algorthim("ALGORITHM_FACE_RECOGNITION")
				time.sleep(1)
			write_dot(all_down_data)

# money classification - face recognition
	if(SwitchMode == 3):
# 		write_dot(DAEKI) 
		        
		try:
			#hl.algorthim("ALGORITHM_FACE_RECOGNITION")
			#time.sleep(0.3)
			if(type(hl.requestAll()[0]) != int):
				money_num = hl.requestAll()[0].__dict__['ID']
				if(money_num == 1):
					print(f"1000won")
					write_dot(CHEON) 
					time.sleep(2)
					write_dot(all_down_data)
				elif(money_num == 2):
					print(f"5000won")
					write_dot(OHCHEON) 
					time.sleep(2)
					write_dot(all_down_data)
				elif(money_num == 3):
					print(f"10000won")
					write_dot(MANN) 
					time.sleep(2)
					write_dot(all_down_data)
				elif(money_num > 3):
					print(f"50000won")
					write_dot(OHMANN) 
					time.sleep(2)
					write_dot(all_down_data)
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
			try:
				print("ashing machine!")
				client.call('send', 13)
				write_dot(SETACKI)
				time.sleep(3)
				write_dot(all_down_data)
			except Exception as e:
				print('no server!')
			# return to default setting(non-IoTMode)
			IoTMode = 0
		else:
			if SwitchMode == 4:
				SwitchMode = 0
			else:
				SwitchMode = 4
				hl.algorthim("ALGORITHM_OBJECT_CLASSIFICATION")
				time.sleep(0.3)
			write_dot(all_down_data)

# Traffic light - object classification & color recognition
	if(SwitchMode == 4):
# 		write_dot(DAEKI)
		try:
# 			hl.algorthim("ALGORITHM_OBJECT_CLASSIFICATION")
# 			time.sleep(0.3)
			if(type(hl.requestAll()[0]) != int):
				temp = hl.requestAll()[0].__dict__['ID']
			if(temp == True):
				temp=False
				hl.algorthim("ALGORITHM_COLOR_RECOGNITION")
				time.sleep(0.3)
				if(type(hl.requestAll()[0]) != int):
					trfc_light = hl.requestAll()[0].__dict__['ID']
					if(trfc_light > 3):
						print(f"stopppppp")
						write_dot(RED)
						time.sleep(2)
						write_dot(all_down_data)
					elif(trfc_light >= 1) & (trfc_light <=3):
						print(f"goooooooo")
						write_dot(GREEN)
						time.sleep(2)
						write_dot(all_down_data)
				hl.algorthim("ALGORITHM_OBJECT_CLASSIFICATION")
				time.sleep(0.3)
		except KeyboardInterrupt:
			print("\nQUITING")
			quit()
		except IndexError:
			print(f"cc")
		except Exception as e:
			print(f"Error {e}")   