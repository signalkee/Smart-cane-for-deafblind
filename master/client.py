import msgpackrpc
import time
client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 3321))

while(1):
    client.call('send', 1)
    result = client.call('readsend',1)
    print(result)
    time.sleep(3)
    client.call('send', 2)  
    result = client.call('readsend',1)
    print(result)
    time.sleep(3)
    client.call('send', 0)  
    result = client.call('readsend',1)
    print(result)
    time.sleep(3)
    
