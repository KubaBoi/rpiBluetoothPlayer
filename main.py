from http.server import HTTPServer
import threading
import webbrowser
import time
import pyautogui

from bluetoothController import BluetoothController
from server import Server

bController = BluetoothController()
thread = threading.Thread(target=bController.serveForever, args=())
thread.start()

server = HTTPServer(("localhost", 8000), Server)
thread2 = threading.Thread(target=server.serve_forever, args=())
thread2.start()

time.sleep(1)
pyautogui.press("Enter")
webbrowser.open("http://localhost:8000")
time.sleep(10)
pyautogui.press("F11")

while True:
    pass
