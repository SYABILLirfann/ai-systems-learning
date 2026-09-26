import sqlite3

connection = sqlite3.connect("player_database.db")
db_worker = connection.cursor()


db_worker.execute("""
CREATE TABLE IF NOT EXISTS players (
    name TEXT,
    position TEXT,
    club TEXT,
    goals INTEGER,
    assists INTEGER,
    foot TEXT
)
""")



def add_player():
    name = input("Enter player name: ")
    position = input("Enter position: ")
    club = input("Enter club: ")
    goals = int(input("Enter player goals: "))
    assists = int(input("Enter player assists: "))
    foot = input("Enter player foot: ")

    db_worker.execute(
    "INSERT INTO players (name, position, club, goals, assists, foot) VALUES (?, ?, ?, ?, ?, ?)",
    (name, position, club, goals, assists, foot)
    )

    connection.commit()


def view_players():
    db_worker.execute("SELECT * FROM players")
    players = db_worker.fetchall()

   
    for player in players:
      print(f"Name: {player[0]}")
      print(f"Position: {player[1]}")
      print(f"Club: {player[2]}")
      print(f"Goals: {player[3]}")
      print(f"Assists: {player[4]}")
      print(f"Foot: {player[5]}")


def search_player():
    name = input("Enter player name: ")

    db_worker.execute(
        "SELECT * FROM players WHERE name = ?",
        (name,)
    )

    player = db_worker.fetchone()

    if player:
       print(f"Name: {player[0]}")
       print(f"Position: {player[1]}")
       print(f"Club: {player[2]}")
       print(f"Goals: {player[3]}")
       print(f"Assists: {player[4]}")
       print(f"Foot: {player[5]}")
    else:
       print("Player not found.")


def update_player():
    name = input("Enter player name: ")
    new_club = input("Enter new club: ")

    db_worker.execute(
    "UPDATE players SET club = ? WHERE name = ?",
    (new_club, name)
    )

    connection.commit()


def delete_player():
    name = input("Enter player name: ")
   
    db_worker.execute(
        "DELETE FROM players WHERE name = ?",
        (name,)
        )

    connection.commit()


print("FOOTBALL SQUAD MANAGER")
print("1. Add Player")
print("2. View Player")
print("3. Search player")
print("4. Update Player")
print("5. Delete Player")


choice = input("Choose an option: ")

if choice == "1":
    add_player()

elif choice == "2":
     view_players()

elif choice == "3":
    search_player()

elif choice == "4":
    update_player()

elif choice == "5":
    delete_player()

else:
    print("Invalid option.")