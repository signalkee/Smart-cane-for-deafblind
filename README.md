# Deafblind_device_hackathon
3rd national rehabilitation center device hackathon for deaf-blind

Team - 혼자서도 잘하조  
Leader - 이종복  
Team - 김선우, 기인호, 김상도

## Dependency
### Master(Cane) raspberrypi
```
 pip3 install random    
 pip3 install msgpack-rpc-python      
 pip3 install time     
 pip3 install huskylib     
```

### Slave(IoT system) raspberrypi
```
pip3 install random     
pip3 install msgpack-rpc-python     
pip3 install time     
pip3 install huskylib     
pip3 install pygame     
```

## Auto start
### Master
```
sudo vi /etc/xdg/lxsession/LXDE-pi/autostart   
   
@sudo /home/hz/Desktop/client    
@/usr/bin/python3 /home/hz/Desktop/master_main.py   
#need to change to your directory
```

### Slave
```
sudo vi /etc/xdg/lxsession/LXDE-pi/autostart   
    
@sudo /home/hz/Desktop/simple_test
@/usr/bin/python3 /home/hz/Desktop/slave_main.py    
#need to change to your directory
```

    
## 3d model
<img src="https://user-images.githubusercontent.com/41245985/55308508-ee840300-5495-11e9-9725-1348480ac39c.PNG" width="90%"></img>

## product
<img src="https://user-images.githubusercontent.com/41245985/55308915-16c03180-5497-11e9-9f1e-ca2fd453adea.png" width="90%"></img>

## hardware list
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

## hackathon poster
<img src="https://user-images.githubusercontent.com/41769238/187227556-c47e390f-88bd-43a0-a315-b4da69071ff2.png" width="90%"></img>
<img src="https://user-images.githubusercontent.com/41769238/187227565-e666563c-b61f-4928-a4c0-e60d37e2fba3.png" width="90%"></img>


