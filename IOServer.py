from socket import *
from PIL import ImageGrab
from PIL import Image
from io import BytesIO
import time
import pyautogui

server_ip = "10.0.0.135"
server_port = 12001
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(100)

while True:
    client_socket, client_address = server_socket.accept()
    print("Request received")
    data = client_socket.recv(2048)
    message = data.decode()
    splitMessage = message.split(" ")
    
    if (splitMessage[0] == "lc"):
        print(f"clicking at: {splitMessage[1]}, {splitMessage[2]}")
        pyautogui.click(int(splitMessage[1]), int(splitMessage[2]))
        
    client_socket.close()
    
server_socket.close()
    