import zmq
import json
from threading import Thread

def bind_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:4554")
