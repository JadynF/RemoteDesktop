from socket import *
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
import keyboard
import pygetwindow

serverIp = "10.0.0.237"
skipTime = time.time()
mouseMoveDelay = 0.1

def mouseEvent(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        print(f"left down at: {x}, {y}")
        message = f"ld {x} {y}"
        socket2.send(message.encode())
        socket2.close()
    elif event == cv2.EVENT_LBUTTONUP:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        print(f"left up at: {x}, {y}")
        message = f"lu {x} {y}"
        socket2.send(message.encode())
        socket2.close()
    elif event == cv2.EVENT_RBUTTONDOWN:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        print(f"right down at: {x}, {y}")
        message = f"rd {x} {y}"
        socket2.send(message.encode())
        socket2.close()
    elif event == cv2.EVENT_RBUTTONUP:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        print(f"right up at: {x}, {y}")
        message = f"ru {x} {y}"
        socket2.send(message.encode())
        socket2.close()
    elif event == cv2.EVENT_MOUSEWHEEL:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        delta = flags >> 16
        message = ""
        print("scroll event")
        if delta > 0:
            print("Scrolled up")
            message = "ms u"
        else:
            print("Scrolled down")
            message = "ms d"
        socket2.send(message.encode())
        socket2.close()
    elif event == cv2.EVENT_MOUSEMOVE:
        global skipTime
        nowTime = time.time()
        if nowTime - skipTime > mouseMoveDelay:
            socket2 = socket(AF_INET, SOCK_STREAM)
            socket2.connect((serverIp, 12001))
            message = f"mm {x} {y}"
            socket2.send(message.encode())
            socket2.close()
            skipTime = time.time()
            mousePos = [x, y]
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        print(f"double click: {x}, {y}")
        message = f"dl {x} {y}"
        socket2.send(message.encode())
        socket2.close()
        
def keyboardEvent(event):
    if (pygetwindow.getActiveWindow().title == "video"):
        #print(f"keypress at: {event.name}")
        socket2 = socket(AF_INET, SOCK_STREAM)
        socket2.connect((serverIp, 12001))
        message = f"kp {event.name}"
        socket2.send(message.encode())
        socket2.close()
    
#def keyboardEvent(key):
#    print(f"keypress at: {chr(key)}")
#    socket2 = socket(AF_INET, SOCK_STREAM)
#    socket2.connect(("10.0.0.237", 12001))
#    message = f"kp {chr(key)}"
#    socket2.send(message.encode())
#    socket2.close()

def videoConnection():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((serverIp, 12000))
    message = "Hello"
    
    client_socket.send(message.encode())
    
    cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("video", mouseEvent)
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
                cv2.waitKey(1)
                #key = cv2.waitKey(1)
                #if key != -1:
                #    keyboardEvent(key)
                #print("Displayed")
            byteString = frames[framesLen - 1]        
        
    client_socket.close()
    cv2.destroyAllWindows()
    time.sleep(1)
    
def main():
    keyboard.on_press(keyboardEvent)
    while True:
        videoConnection()
        
main()

