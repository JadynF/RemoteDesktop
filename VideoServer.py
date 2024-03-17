from socket import *
from PIL import ImageGrab
from PIL import Image
from io import BytesIO
import time
import struct

server_ip = "10.0.0.171"
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(100)

while True:
    client_socket, client_address = server_socket.accept()
    print("Request received")
    rec = client_socket.recv(2048)
    
    #if rec.decode() != "Saysay12!":
    #    print("Failed authentication")
    #    continue
    
    imgQuality = 75
    
    try:
        while True:
            #rec = client_socket.recv(2048)
            
            image = ImageGrab.grab()
            
            bytes = BytesIO()
            image.save(bytes, "JPEG", quality=imgQuality, subsampling=0)
            
            #print(len(bytes.getvalue()))
            
            client_socket.send(struct.pack("!I", len(bytes.getvalue())))
            client_socket.send(bytes.getvalue())
            time.sleep(0.016)
    except:
        print("closing connection")
        
    client_socket.close()
    