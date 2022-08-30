# Deafblind_device_hackathon
3rd national rehabilitation center device hackathon for deaf-blind

Product name - EYE    
Team name - Do It Alone  
Leader - JB LEE  
Team - SW KIM, IH KEE, SD KIM

Product name - 세상을 보는 눈   
Team name - 혼자서도 잘하조  
Leader - 이종복  
Team - 김선우, 기인호, 김상도

## Overall product summary
<img src="https://user-images.githubusercontent.com/41769238/187329859-dacca075-294a-41b6-8974-2fcac7f3d13b.png" width="100%"></img>

## What & Why (Included features)
@@ need to add poster image

## 3D model
<img src="https://user-images.githubusercontent.com/41769238/187233177-0179fb16-1ae2-43b0-9ebe-1cd48d6d107b.png" width="60%"></img>
<img src="https://user-images.githubusercontent.com/41769238/187233165-c408e862-5ca7-48f4-af45-fe1b82cfd5b7.png" width="60%"></img>
<img src="https://user-images.githubusercontent.com/41769238/187233174-ec815071-a689-4df4-beea-48101546c60f.png" width="60%"></img>

## Module assembly diagram
<img src="https://user-images.githubusercontent.com/41769238/187329878-73434c28-6c5d-4806-821c-b8774560256b.png" width="100%"></img>

## Pin map
<img src="https://user-images.githubusercontent.com/41769238/187330582-d0b20a61-d0af-4f7f-b79f-0c695d23a685.png" width="100%"></img>

## Hardware list
Foldable cane - 1 pcs  
Raspberry-pi 4 - 1 pcs   
Raspberry-pi 3 b+ - 1pcs   
Huskey lens - 2 pcs     
vibration motor - 1 pcs     
2cell Lipo - 1 pcs    
switch - 6 pcs    
voltage step down module - 2 pcs    
usb C to usb A cable - 2 pcs    
Dot cell module - 1pcs  

## Dependency
### Master(Cane) raspberrypi
```
pip3 install random    
pip3 install msgpack-rpc-python      
pip3 install time     
pip3 install huskylib    
pip3 install pypng     
apt install libblutooth-dev    
```

### Slave(IoT system) raspberrypi
```
pip3 install random     
pip3 install msgpack-rpc-python     
pip3 install time     
pip3 install huskylib     
pip3 install pygame     
pip3 install pypng    
apt install libblutooth-dev    
```

## Auto start
### Master(Cane) raspberrypi
```
sudo vi /etc/xdg/lxsession/LXDE-pi/autostart   
   
@sudo /home/hz/Desktop/client    
@/usr/bin/python3 /home/hz/Desktop/master_main.py   
#need to change to your directory
```

### Slave(IoT system) raspberrypi
```
sudo vi /etc/xdg/lxsession/LXDE-pi/autostart   
    
@sudo /home/hz/Desktop/simple_test
@/usr/bin/python3 /home/hz/Desktop/slave_main.py    
#need to change to your directory
```
## For Independent Cane usage
You should remove several codes in master_main.py

```
# line num 5
client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))

# line num 43~50
	doorbell = client.call('readsend', 1)
	if doorbell != last_doorbel:
		doorbell = doorbell % 5
		print(f"{nameList[doorbell]} arrive!")
		GPIO.output(vib, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(vib, GPIO.LOW)
		last_doorbell = doorbell


```
    

## Hackathon poster
<img src="https://user-images.githubusercontent.com/41769238/187227556-c47e390f-88bd-43a0-a315-b4da69071ff2.png" width="90%"></img>
<img src="https://user-images.githubusercontent.com/41769238/187227565-e666563c-b61f-4928-a4c0-e60d37e2fba3.png" width="90%"></img>


