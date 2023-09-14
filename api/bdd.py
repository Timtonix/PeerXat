import sqlite3

con = sqlite3.connect("peer.db")
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS peers(pseudo VARCHAR(20), ip VARCHAR(20), port VARCHAR(6), date_connection TEXT)")

