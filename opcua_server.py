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

parser = argparse.ArgumentParser(description="Esempio di parsing coppie chiave-valore")
parser.add_argument("-p", "--port", required=False, default=4840, help="port")
parser.add_argument("-i", "--interface", required=False, default="0.0.0.0", help="Listen interface")
default_urn=random_string(5)
parser.add_argument("-u", "--urn", required=False, default=default_urn, help="URN")
parser.add_argument("-n", "--name", required=False, default="OPC-UA Server", help="Server name")

args = parser.parse_args()

# Create server
server = Server()
server.set_endpoint(f"opc.tcp://{args.interface}:{args.port}")
server.set_server_name(args.name)
server.load_certificate("./certs/server-certificate.pem")
server.load_private_key("./certs/server-private-key.pem")

# Register namespace
idx = server.register_namespace("{args.urn}")

# Add object and variable
objects = server.get_objects_node()
device = objects.add_object(idx, "MyDevice")
temperature = device.add_variable(idx, "Temperature", 20.0)
temperature.set_writable()

# Start server
server.start()
print("OPC UA Server running at opc.tcp://0.0.0.0:4840")

try:
    while True:
        val = temperature.get_value() + 0.1
        temperature.set_value(val)
        print("Updated Temperature:", val)
        time.sleep(1)

except KeyboardInterrupt:
    print("Shutting down server...")
    server.stop()
