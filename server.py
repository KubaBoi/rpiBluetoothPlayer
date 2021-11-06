from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os.path
from os import path, listdir
import pathlib
import datetime
import json
import threading

from bluetoothController import BluetoothController

hostName = "localhost"
hostPort = 8000

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/"):
            self.sendFile("index.html")

        elif (self.path == "/update"):
            self.update()

    def do_POST(self):
        if (self.path == "/update"):
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            self.sendMessage(post_body)

    def sendFile(self, file):
        if (not path.exists(file)):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(file, "rb") as f:
            self.wfile.write(f.read())

    def update(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        with open("data.json", "rb") as f:
            self.wfile.write(f.read())


import webbrowser

webbrowser.open("http://localhost:8000")

myServer = HTTPServer((hostName, hostPort), Server)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    bController = BluetoothController()
    thread = threading.Thread(target=bController.serveForever, args=())
    thread.start()

    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))