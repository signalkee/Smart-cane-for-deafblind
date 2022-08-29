import msgpackrpc
import time
client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))

while(1):
    client.call('sendtoCANE', 1)  
    time.sleep(3)
    client.call('sendtoCANE', 2)  
    time.sleep(3)
    client.call('sendtoCANE', 0)  
    time.sleep(3)
    
