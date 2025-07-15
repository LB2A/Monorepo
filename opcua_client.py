#!/usr/bin/env python3
from opcua import Client
import argparse

parser = argparse.ArgumentParser(description="Simple OPC UA Client")
parser.add_argument("-e", "--endpoint", default="opc.tcp://127.0.0.1:4840", help="OPC UA server endpoint")
parser.add_argument("-n", "--nodeid", default="ns=2;s=MyDevice.Temperature", help="NodeId to read")
parser.add_argument("-c", "--cert", default="opc-ua_certificate.pem", help="Server certificate to trust (PEM)")

args = parser.parse_args()
client = Client(args.endpoint)
client.set_security_string(f"Basic256Sha256,SignAndEncrypt,{args.cert},opc-ua_private-key.pem,opc-ua_certificate.pem")

try:
    client.connect()
    print(f"Connected to {args.endpoint}")
    node = client.get_node(args.nodeid)
    value = node.get_value()
    print(f"Value of {args.nodeid}: {value}")

finally:
    client.disconnect()
    print("Disconnected.")
