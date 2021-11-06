from http.server import HTTPServer
import threading
import webbrowser
import time
import os
import dbus

from bluetoothController import BluetoothController
from server import Server

bus = dbus.SystemBus()

player = bus.get_object('org.bluez','/org/bluez/hci0/dev_78_6A_89_FA_1C_95/player0')
BT_Media_iface = dbus.Interface(player, dbus_interface='org.bluez.MediaPlayer1')
BT_Media_props = dbus.Interface(player, "org.freedesktop.DBus.Properties")

props = BT_Media_props.GetAll("org.bluez.MediaPlayer1") 

"""bController = BluetoothController()
thread = threading.Thread(target=bController.serveForever, args=())
thread.start()

server = HTTPServer(("localhost", 8000), Server)
thread2 = threading.Thread(target=server.serve_forever, args=())
thread2.start()
"""
"""import pyautogui
webbrowser.open("http://localhost:8000")
time.sleep(10)
pyautogui.press("F11")

while True:
    if os.path.exists("status.txt"):
        with open("status.txt", "r") as f:
            data = f.read()
            if (data == "0"):
                bController.pause()
            elif (data == "1"):
                bController.play()
            elif (data == "2"):
                bController.prev()
            elif (data == "3"):
                bController.next()

        os.remove("status.txt")"""
