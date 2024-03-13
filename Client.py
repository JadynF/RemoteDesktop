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
import struct

serverIp = "192.168.1.59"
skipTime = time.time()
mouseMoveDelay = 0.1

def mouseEvent(event, x, y, flags, params):
    socket2 = socket(AF_INET, SOCK_STREAM)
    socket2.connect((serverIp, 12001))
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"left down at: {x}, {y}")
        message = f"ld {x} {y}"
        socket2.send(message.encode())
    elif event == cv2.EVENT_LBUTTONUP:
        print(f"left up at: {x}, {y}")
        message = f"lu {x} {y}"
        socket2.send(message.encode())
    elif event == cv2.EVENT_RBUTTONDOWN:
        print(f"right down at: {x}, {y}")
        message = f"rd {x} {y}"
        socket2.send(message.encode())
    elif event == cv2.EVENT_RBUTTONUP:
        print(f"right up at: {x}, {y}")
        message = f"ru {x} {y}"
        socket2.send(message.encode())
    elif event == cv2.EVENT_MOUSEWHEEL:
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
    elif event == cv2.EVENT_MOUSEMOVE:
        global skipTime
        nowTime = time.time()
        if nowTime - skipTime > mouseMoveDelay:
            message = f"mm {x} {y}"
            socket2.send(message.encode())
            skipTime = time.time()
            mousePos = [x, y]
    elif event == cv2.EVENT_LBUTTONDBLCLK:
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

def videoConnection():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((serverIp, 12000))
    message = "Saysay12!"
    
    client_socket.send(message.encode())
    
    cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("video", mouseEvent)
    
    while True:
        #print("Received")
        frameLengthData = client_socket.recv(4)
        if not frameLengthData:
            break
        frameLength = struct.unpack("!I", frameLengthData)[0]
        
        byteString = b''
        while len(byteString) < frameLength:
            frameChunk = client_socket.recv(frameLength - len(byteString))
            if not frameChunk:
                break
            byteString += frameChunk

        nparr = np.frombuffer(byteString, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow("video", frame)
        cv2.waitKey(1)
        
    client_socket.close()
    cv2.destroyAllWindows()
    time.sleep(1)
    
def main():
    keyboard.on_press(keyboardEvent)
    while True:
        videoConnection()
        
main()

