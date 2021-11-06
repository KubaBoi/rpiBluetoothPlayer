import threading

from bluetoothController import BluetoothController

bController = BluetoothController()
bController.serveForever()
#thread = threading.Thread(target=bController.serveForever, args=())
#thread.start()

while True:
    pass