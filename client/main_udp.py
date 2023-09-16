from api import udp_api as udp
import threading


client = udp.UDPClient("fatboy")

receiver = threading.Thread(target=client.receiver)
receiver.start()