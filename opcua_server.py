#!/usr/bin/env python3
from opcua import Server
from datetime import datetime
import time
import sys
import argparse
import random
import string

def random_string(length):
    alphabet = string.ascii_letters  # a-z + A-Z
    return ''.join(random.choices(alphabet, k=length))

def increase_temperature(device):
    current_temp = device_temperature.get_value()
    device_temperature.set_value(current_temp + 1)


parser = argparse.ArgumentParser(description="Esempio di parsing coppie chiave-valore")
parser.add_argument("-p", "--port", required=False, default=4840, help="port")
parser.add_argument("-i", "--interface", required=False, default="0.0.0.0", help="Listen interface")
default_urn=random_string(5)
parser.add_argument("-u", "--urn", required=False, default=default_urn, help="URN")
parser.add_argument("-n", "--name", required=False, default="OPC-UA Server", help="Server name")
args = parser.parse_args()


server = Server()
server.set_endpoint(f"opc.tcp://{args.interface}:{args.port}")
server.set_server_name(args.name)
server.load_certificate("./certs/server-certificate.pem")
server.load_private_key("./certs/server-private-key.pem")
idx = server.register_namespace("{args.urn}")
objects = server.get_objects_node()

#Insert objects here
device = objects.add_object(idx, "MyDevice")
device_temperature = device.add_variable(idx, "Temperature", 20.0)
device_temperature.set_writable()

server.start()
print(f"OPC UA Server running at opc.tcp://{args.interface}:{args.port}")
try:
    while True:
        #Implement here
        

except KeyboardInterrupt:
    print("Shutting down server...")
    server.stop()
