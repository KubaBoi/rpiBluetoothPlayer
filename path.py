import os
class Path:
    def __init__(self):
        if os.path.exists(f"{os.getcwd()}/rpiBluetoothPlayer/main.txt"):
            self.path = f"{os.getcwd()}/rpiBluetoothPlayer/"
        elif os.path.exists(f"{os.getcwd()}/main.txt"):
            self.path = f"{os.getcwd()}/"
        else:
            self.path = ":("

    def getPath(self):
        return self.path