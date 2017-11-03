#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """

import logging
import socket
import sys
#import requests
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import webserver
g_ip = '0.0.0.0'
def on_service_state_change(zeroconf, service_type, name, state_change):
    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            global g_ip
            g_ip = socket.inet_ntoa(info.address)
            print("  Address: %s:%d" % (g_ip, info.port))
            print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            print("  Server: %s" % (info.server,))
            webserver.setIP(g_ip)
            #r = requests.get('https://' + g_ip + g_port + '/?extension=advance' + '&name=Head_movement' + '&p1=30' + '&p2=30')
            #payload = {'extension': 'advance' ,  'name': 'Get_sentences'}
            #r = requests.get('http://' + g_ip + g_port, params = payload)
            #print("url = %s" % (r.url))
        else:
            print("  No info")
        print('\n')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()