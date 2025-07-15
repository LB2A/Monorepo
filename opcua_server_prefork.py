#!/usr/bin/env python3
import socket
import os
import signal
from opcua import Server
from datetime import datetime
import time
import argparse
import random
import string
import sys

def random_string(length):
    alphabet = string.ascii_letters
    return ''.join(random.choices(alphabet, k=length))

def setup_opcua_server(interface, port, name, urn, temperature_val):
    server = Server()
    server.set_endpoint(f"opc.tcp://{interface}:{port}")
    server.set_server_name(name)
    server.load_certificate("./certs/server-certificate.pem")
    server.load_private_key("./certs/server-private-key.pem")
    idx = server.register_namespace(urn)
    objects = server.get_objects_node()
    device = objects.add_object(idx, "MyDevice")
    device_temperature = device.add_variable(idx, "Temperature", temperature_val)
    device_temperature.set_writable()
    return server, device_temperature

parser = argparse.ArgumentParser(description="Prefork OPC UA Server")
parser.add_argument("-p", "--port", type=int, default=4840, help="Port")
parser.add_argument("-i", "--interface", default="0.0.0.0", help="Listen interface")
default_urn = random_string(5)
parser.add_argument("-u", "--urn", default=default_urn, help="URN")
parser.add_argument("-n", "--name", default="OPC-UA Server", help="Server name")
args = parser.parse_args()

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind((args.interface, args.port))
listen_sock.listen(5)

print(f"Prefork OPC UA master listening on {args.interface}:{args.port}")

def reap_children(signum, frame):
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except ChildProcessError:
            break

signal.signal(signal.SIGCHLD, reap_children)

while True:
    conn, addr = listen_sock.accept()
    print(f"Connection from {addr[0]}")

    pid = os.fork()
    if pid == 0:
        listen_sock.close()
        conn.close()

        child_port = random.randint(50000, 60000)
        server, device_temperature = setup_opcua_server("0.0.0.0", child_port, args.name, args.urn, 20.0)
        print(f"[{os.getpid()}] Child OPC UA Server on port {child_port} for {addr[0]}")
        try:
            server.start()
            while True:
                temp = device_temperature.get_value()
                device_temperature.set_value(temp + 1)
                print(f"[{os.getpid()}] Updated Temperature: {device_temperature.get_value()}")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"[{os.getpid()}] Shutting down...")
        finally:
            server.stop()
            os._exit(0)
    else:
        conn.close()
