from http.server import HTTPServer
import threading
import webbrowser

from bluetoothController import BluetoothController
from server import Server

bController = BluetoothController()
thread = threading.Thread(target=bController.serveForever, args=())
thread.start()

server = HTTPServer(("localhost", 8000), Server)
thread2 = threading.Thread(target=server.serveForever, args=())
thread2.start()


webbrowser.open("http://localhost:8000")

while True:
    pass