from socket import *
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
import keyboard

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect(("10.0.0.237", 12001))
        print(f"left click at: {x}, {y}")
        message = f"lc {x} {y}"
        socket2.send(message.encode())
        socket2.close()
    elif event == cv2.EVENT_RBUTTONDOWN:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect(("10.0.0.237", 12001))
        print(f"right click at: {x}, {y}")
        message = f"rc {x} {y}"
        socket2.send(message.encode())
        socket2.close()
        
def keyboard_event(event):
    print(f"keypress at: {event.name}")
    socket2 = socket(AF_INET, SOCK_STREAM)
    socket2.connect(("10.0.0.237", 12001))
    message = f"kp {event.name}"
    socket2.send(message.encode())
    socket2.close()
        
def videoConnection():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(("10.0.0.237", 12000))
    message = "Hello"
    
    client_socket.send(message.encode())
    
    cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("video", click_event)
    lossCount = 0
    
    byteString = b''
    while True:
        #print("Received")
        bytes = client_socket.recv(1000000)
        byteString += bytes
        frames = byteString.split(b' end ')
        framesLen = len(frames)
        if (framesLen > 1):
            for i in range(framesLen - 1):
                nparr = np.frombuffer(frames[i], np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow("video", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                #print("Displayed")
            byteString = frames[framesLen - 1]        
        
    client_socket.close()
    cv2.destroyAllWindows()
    time.sleep(1)
    
def main():
    keyboard.on_press(keyboard_event)
    while True:
        videoConnection()
        
main()

