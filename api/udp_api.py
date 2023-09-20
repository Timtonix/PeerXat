import socket
import netifaces
import time
import api.utils as utils


def get_hostname() -> dict:
    """
    use netifaces to discover your interfaces.
    Check for the first Interface that have an afinet IP and a broadcat

    :return: A dict with the broadcast and the local Ip address
    """
    for interface in netifaces.interfaces():
        if interface.startswith(("lo", "docker", "vbox")):
            continue
        details = netifaces.ifaddresses(interface)
        try:
            broadcast = {"broadcast": details[netifaces.AF_INET][0]["broadcast"], "afinet": details[netifaces.AF_INET][0]["addr"]}
            return broadcast
        except KeyError:
            print(f"L'interface {interface} n'a pas d'adresse AF_INET")


class UDPClient:
    def __init__(self, name, port=50001, reachable: str = "on", discoverable: str = "on"):
        self.name = name
        self.port = port
        self.client_ip = get_hostname()
        self.split_ip = list(map(int, self.client_ip["broadcast"].split(".")))

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
                if self.client_ip["afinet"] != ip:
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
                if not utils.handle_connection(data, addr):
                    print(f"Someone wants to fight !")
            elif data.startswith("pong"):
                if not utils.handle_connection(data, addr):
                    print(f"Someone wants to fight !")
            else:
                print(data)

    def sender(self, message: str, ip: str, port: int = 50001):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        request = f"{message}".encode()
        try:
            sock.sendto(request, (ip, port))
        except OSError as e:
            print(e)




if __name__ == "__main__":
    client = UDPClient("timtonix", 50001)
    print(client.client_ip)