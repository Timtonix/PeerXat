from api import udp_api as udp
import threading


client = udp.UDPClient("fatboy")
print(client.client_ip)
receiver = threading.Thread(target=client.receiver)
receiver.start()
client.scanner()