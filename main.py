import sqlite3

connection = sqlite3.connect("player_database.db")

db_worker = connection.cursor()


db_worker.execute("""
CREATE TABLE IF NOT EXISTS players (
    name TEXT,
    position TEXT,
    club TEXT,
    goals INTEGER,
    assists INTEGER
    foot TEXT
)
""")
#db_worker.execute(
#    "ALTER TABLE players ADD COLUMN foot TEXT"
#)

name = input("Enter player name: ")
position = input("Enter position: ")
club = input("Enter club: ")
goals = int(input("Enter goals: "))
assists = int(input("Enter assists: "))
foot = (input("Enter Foot: "))


db_worker.execute(
    "INSERT INTO players (name, position, club, goals, assists, foot) VALUES (?, ?, ?, ?, ?, ?)",
  (name, position, club, goals, assists, foot)
   )

db_worker.execute(
    "UPDATE players SET foot = ? WHERE name = ?",
    ("left", "Messi")
)

connection.commit()

connection.commit()

db_worker.execute("SELECT * FROM players")

players = db_worker.fetchall()


for player in players:
    print(f"Name: {player[0]}")
    print(f"Position: {player[1]}")
    print(f"Club: {player[2]}")
    print(f"Goals: {player[3]}")
    print(f"Assists: {player[4]}")
    print(f"Foot: {player[5]}")

connection.close()
