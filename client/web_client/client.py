import zmq
from threading import Thread
import json
import asyncio


def connect_to_the_server():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:4554")


def main(pseudo):
    pass
