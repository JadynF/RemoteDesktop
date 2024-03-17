from socket import *
from PIL import ImageGrab
from PIL import Image
from io import BytesIO
import time
import pyautogui

server_ip = "10.0.0.171"
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
    
    if (splitMessage[0] == "dl"):
        print("double clicking")
        pyautogui.click(int(splitMessage[1]), int(splitMessage[2]))
    elif (splitMessage[0] == "ld"):
        print(f"clicking left down: {splitMessage[1]}, {splitMessage[2]}")
        pyautogui.mouseDown(button = "left", x = int(splitMessage[1]), y = int(splitMessage[2]))
    elif (splitMessage[0] == "lu"):
        print(f"clicking left up: {splitMessage[1]}, {splitMessage[2]}")
        pyautogui.mouseUp(button = "left", x = int(splitMessage[1]), y = int(splitMessage[2]))
    elif (splitMessage[0] == "rd"):
        print(f"clicking right down: {splitMessage[1]}, {splitMessage[2]}")
        pyautogui.mouseDown(button = "right", x = int(splitMessage[1]), y = int(splitMessage[2]))
    elif (splitMessage[0] == "ru"):
        print(f"clicking right up: {splitMessage[1]}, {splitMessage[2]}")
        pyautogui.mouseUp(button = "right", x = int(splitMessage[1]), y = int(splitMessage[2]))
    elif (splitMessage[0] == "kd"):
        print(f"down key: {splitMessage[1]}")
        pyautogui.keyDown(splitMessage[1])
    elif (splitMessage[0] == "ku"):
        print(f"up key: {splitMessage[1]}")
        pyautogui.keyUp(splitMessage[1])
    elif (splitMessage[0] == "ms"):
        if (splitMessage[1] == "u"):
            print("scrolling up")
            pyautogui.scroll(100)
        elif (splitMessage[1] == "d"):
            print("scrolling down")
            pyautogui.scroll(-100)
    elif (splitMessage[0] == "mm"):
        pyautogui.moveTo(int(splitMessage[1]), int(splitMessage[2]), 0.1)
        
    client_socket.close()
    
server_socket.close()
    