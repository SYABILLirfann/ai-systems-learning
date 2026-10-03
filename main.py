import sqlite3
from openai import OpenAI, AuthenticationError
from pydantic import BaseModel, Field

class PlayerAnalysis(BaseModel):
    player: str
    rating: int = Field(ge=1, le=10)
    strength: str
    rating_reason: str


def analyze_player(client, name, position, club, goals, assists):

    response = client.responses.parse(
        model="gpt-5.4-mini",
        input=f"""
Analyze this football player using the supplied stats.

Player: {name}
Position: {position}
Club: {club}
Goals: {goals}
Assists: {assists}

Give the player a rating from 1 to 10, identify one main strength, and explain why you gave that rating.
""",
        text_format=PlayerAnalysis
    )

    return response.output_parsed

def save_analysis(db_worker, db, name, rating, strength, rating_reason):
    db_worker.execute(
        "UPDATE players SET ai_rating = ?, ai_strength = ?, ai_rating_reason = ? WHERE name = ?",
        (rating, strength, rating_reason, name)
    )

    db.commit()

def find_player(db_worker, player_name):
    db_worker.execute(
        "SELECT * FROM players WHERE LOWER(name) = LOWER(?)",
        (player_name,)
    )

    return db_worker.fetchone()

def get_top_scorers(db_worker):
    db_worker.execute(
        "SELECT * FROM players ORDER BY goals DESC LIMIT 5"
    )

    return db_worker.fetchall()

def get_high_performers(db_worker, minimum_goals, minimum_assists):
    db_worker.execute(
        "SELECT * FROM players WHERE goals >= ? AND assists >= ? ORDER BY goals DESC, assists DESC",
        (minimum_goals, minimum_assists)
    )

    return db_worker.fetchall()

def show_menu():
    print("\n--- FOOTBALL SCOUT ---")
    print("1. Scout a player")
    print("2. Show top scorers")
    print("3. Find high performers")
    print("4. Exit")

    return input("Choose an option: ").strip()

def show_high_performers(db_worker):
    try:
        minimum_goals = int(input("Minimum goals: "))
        minimum_assists = int(input("Minimum assists: "))
    except ValueError:
        print("Please enter numbers only.")
        return


    
client = OpenAI()



db = sqlite3.connect("player_database.db")
db_worker = db.cursor()

db_worker.execute("PRAGMA table_info(players)")
columns = db_worker.fetchall()

if "ai_rating_reason" not in [column[1] for column in columns]:
    db_worker.execute(
        "ALTER TABLE players ADD COLUMN ai_rating_reason TEXT"
    )
    db.commit()

while True:
    choice = show_menu()

    if choice == "4":
        break

    elif choice == "1":
        player_name = input("Enter player name: ").strip()

        player_data = find_player(db_worker, player_name)

        if player_data is None:
             print("Player not found.")
             continue


        name = player_data[0]
        position = player_data[1]
        club = player_data[2]
        goals = player_data[3]
        assists = player_data[4]


        try:
            analysis = analyze_player(client, name, position, club, goals, assists)
        except AuthenticationError as e:
            print(f"Authentication failed: {e}")
            db.close()
            exit()


        print("\n--- AI SCOUT REPORT ---")
        print(f"Position: {position}")
        print(f"Club: {club}")
        print(f"Goals: {goals}")
        print(f"Assists: {assists}")
        print(f"Player: {analysis.player}")
        print(f"Rating: {analysis.rating}/10")
        print(f"Main strength: {analysis.strength}")
        print(f"Rating reason: {analysis.rating_reason}")

        save_analysis(
                         db_worker,
                         db,
                         name,
                         analysis.rating,
                         analysis.strength,
                         analysis.rating_reason
                         )

        db_worker.execute(
            "SELECT name, ai_rating, ai_strength, ai_rating_reason FROM players WHERE name = ?",
            (name,)
            )

        saved_player = db_worker.fetchone()
        print(f"Saved to database: {saved_player}")


    elif choice == "2":
         top_scorers = get_top_scorers(db_worker)

         number = 1

         for player in top_scorers:
             print(f"{number}. {player[0]} — {player[3]} goals")
             number += 1

    elif choice == "3":

        try:
              minimum_goals = int(input("Minimum goals: "))
              minimum_assists = int(input("Minimum assists: "))
        except ValueError:
                  print("Please enter numbers only.")
                  continue

        if minimum_goals < 0 or minimum_assists < 0:
           print("Goals and assists cannot be negative.")
           continue

        high_performers = get_high_performers(
            db_worker,
            minimum_goals,
            minimum_assists
        )

        if not high_performers:
           print("No players found matching those requirements.")
           continue

        for player in high_performers:
            print(f"{player[0]} — {player[3]} goals, {player[4]} assists")

    else:
        print("Invalid option. Please choose 1, 2, or 3.")



db.close()