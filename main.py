from http.server import HTTPServer
import threading
import webbrowser
import time
import os

from bluetoothController import BluetoothController
from player import BluePlayer
from server import Server

#bController = BluetoothController()
#thread = threading.Thread(target=bController.serveForever, args=())
#thread.start()

player = BluePlayer()
player.start()
player.pause()

server = HTTPServer(("localhost", 8000), Server)
thread2 = threading.Thread(target=server.serve_forever, args=())
thread2.start()

import pyautogui
webbrowser.open("http://localhost:8000")
time.sleep(10)
pyautogui.press("F11")

while True:
    if os.path.exists("status.txt"):
        with open("status.txt", "r") as f:
            data = f.read()
            if (data == "0"):
                player.pause()
            elif (data == "1"):
                player.play()
            elif (data == "2"):
                player.prev()
            elif (data == "3"):
                player.next()

        os.remove("status.txt")

    