import sqlite3
import datetime

con = sqlite3.connect("peer.db", check_same_thread=False)
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS peers(pseudo VARCHAR(20), ip VARCHAR(20), port INT, date_connection TEXT)")
con.commit()


def add_peer(pseudo: str, ip: str, port: int):
    date = datetime.datetime.now()
    cursor.execute("""INSERT INTO peers(pseudo, ip, port, date_connection) VALUES (?, ?, ?, ?) """, (pseudo, ip, port, date))
    con.commit()


def check_peer(pseudo: str, ip: str, port: int):
    """
    Checks if a peer already exists in the database

    :param pseudo:
    :param ip:
    :param port:
    :return: True if the peer exists, otherwise False
    """
    cursor.execute("""SELECT * FROM peers WHERE pseudo=? AND ip=? AND port=?""", (pseudo, ip, port,))
    row = cursor.fetchall()

    if row:
        return True
    return False
