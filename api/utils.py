import re
import api.bdd as bdd


def handle_connection(data: str, addr: tuple):
    print("HELLLLOOO")
    m = re.match(r"p[i|o]ng (\w+) (\d+)", data)
    if m:
        print(m.groups())
        pseudo = m.group(1)
        port = int(m.group(2))
        ip = addr[0]
        if len(pseudo) < 20 and 50000 < port < 65635:
            bdd.add_peer(pseudo, ip, port)
            return port
    return False
