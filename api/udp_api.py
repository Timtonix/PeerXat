import socket
import netifaces
import time
import api.bdd as bdd
import re


def get_hostname() -> list:
    host = []
    for interface in netifaces.interfaces():
        if interface.startswith(("lo", "docker", "vbox")):
            continue
        details = netifaces.ifaddresses(interface)
        try:
            ip = (details[netifaces.AF_INET][0]["broadcast"], details[netifaces.AF_INET][0]["addr"])
            host.append(details[netifaces.AF_INET][0]["broadcast"])
        except KeyError as e:
            print(f"L'interface {interface} n'a pas d'adresse AF_INET")
    return host


class UDPClient:
    def __init__(self, name, port=50001, reachable: str = "on", discoverable: str = "on"):
        self.name = name
        self.port = port
        self.client_ip = get_hostname()
        self.split_ip = list(map(int, self.client_ip[0][0].split(".")))

        self.peers = {}
        self.discoverable = discoverable
        self.reachable = reachable

    def scanner(self):
        host_list = self.split_ip
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ping_message = f"ping {self.name} {self.port}"
        for i in range(255):
            host_list[3] = i
            ip = ".".join(map(str, host_list))
            try:
                if self.client_ip[0][1] != ip:
                    sock.sendto(ping_message.encode(), (ip, self.port))
            except OSError as e:
                print(f"{ip} except an error : {e}")
            time.sleep(0.05)
        sock.close()

        pass

    def receiver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", self.port))
        print("Receiver have been bound !")
        while True:
            data, addr = sock.recvfrom(1024)
            data = data.decode("utf-8")
            if data.startswith("ping"):
                self.handle_ping(data, addr)
            elif data.startswith("pong"):
                data = data.split(" ")
                print(f"Ponged by {data[1]}")
                print(data)
            else:
                print(data)

    def sender(self, message: str, ip: str, port: int = 50001):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        request = f"{message}".encode()
        try:
            sock.sendto(request, (ip, port))
        except OSError as e:
            print(e)

    def handle_ping(self, data: str, addr: tuple):
        m = re.match(r"ping (\w+) (\d+)", data)
        if m:
            pseudo = m.group(1)
            port = int(m.group(2))
            ip = addr[0]
            print(f"Pinged by {pseudo} {ip}")
            if len(pseudo) < 20 and 50000 < port < 65635:
                bdd.add_peer(pseudo, ip, port)
                message = f"pong {self.name} {self.port}"
                self.sender(message, ip, port)
            else:
                print(" I wont respond to that guy")
        else:
            print("Une personne a essayé de nous envoyer un ping frauduleux")


if __name__ == "__main__":
    client = UDPClient("timtonix", 50001)
    print(client.client_ip)