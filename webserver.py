#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import requests
import urlparse

g_ip = '192.168.0.1.'
g_port = ':8080'
class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

        o = urlparse.urlparse(self.path)
        urlparse.parse_qs(o.query)
        #print("urlparse = %s" % (self.path))
        #print("urlparse.url = %s" % (o.geturl()))
        #print("urlparse = %s" % (urlparse.parse_qs(o.query)))
        payload = {'extension': 'advance',  'name': 'Get_sentences'}
        r = requests.get('http://' + g_ip + g_port, params = urlparse.parse_qs(o.query))
        print("url = %s" % (r.url))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('127.0.0.1', port)
    #global g_port
    #g_port = ':8080'
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

def setIP(ip):
    global g_ip
    g_ip = ip
    run()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()