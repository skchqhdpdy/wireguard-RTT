#tornado==4.4.2?

import os
import tornado.ioloop
import tornado.web
import json
import time
import requests

ServerIP = "175.120.229.31" #vpn.aodd.xyz

class RTTHandler(tornado.web.RequestHandler):
    def get(self):
        if not os.path.isfile("rtt.html"):
            with open("rtt.html", "wb") as f: f.write(requests.get("https://aodd.xyz/wireguard/rtt.html").content)
        self.render("rtt.html")

    def post(self):
        ms = round((time.time() - float(self.request.headers["unixTime"])), 2)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"RTT": ms, "ServerIP": ServerIP, "ClientIP": self.request.headers["X-Real-IP"], "host": self.request.host}, indent=2))

class benchHandler(tornado.web.RequestHandler):
    def get(self):
        if not os.path.isfile("rttbench.html"):
            with open("rttbench.html", "wb") as f: f.write(requests.get("https://aodd.xyz/wireguard/rttbench.html").content)
        self.render("rttbench.html")

def make_app():
    return tornado.web.Application([
        (r"/", benchHandler),
        (r"/rtt", RTTHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    port = 51819
    app.listen(port)
    print(f"Server Listen on http://{ServerIP}:{port} Port | OS = {'Windows' if os.name == 'nt' else 'UNIX'}")
    tornado.ioloop.IOLoop.current().start()