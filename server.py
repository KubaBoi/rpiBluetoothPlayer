from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import path
import json
import os

from path import Path

hostName = "localhost"
hostPort = 8000

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/"):
            self.sendFile("index.html")
        if (self.path == "/sheet.css"):
            self.sendFile("sheet.css", "text/css")

        elif (self.path == "/update"):
            self.update()

    def do_POST(self):
        if (self.path == "/sendUpdate"):
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            pth = Path()
            with open(f"{pth.getPath()}status.txt", "bw") as f:
                f.write(post_body) 
            self.send_response(200)

    def sendFile(self, file, header = "text/html"):
        pth = Path()
        if (not path.exists(f"{pth.getPath()}{file}")):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = f"{pth.getPath()}{file}"
            self.wfile.write(b":(" + f.encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", header)
        self.end_headers()

        with open(f"{pth.getPath()}{file}", "rb") as f:
            self.wfile.write(f.read())

    def update(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        pth = Path()
        with open(f"{pth.getPath()}data.json", "rb") as f:
            self.wfile.write(f.read())


if __name__ == "__main__":
    myServer = HTTPServer((hostName, hostPort), Server)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))