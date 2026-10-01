import sqlite3
from openai import OpenAI, AuthenticationError
from pydantic import BaseModel, Field

class PlayerAnalysis(BaseModel):
    player: str
    rating: int = Field(ge=1, le=10)
    strength: str


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

Give the player a rating from 1 to 10 and identify one main strength.
""",
        text_format=PlayerAnalysis
    )

    return response.output_parsed

def save_analysis(db_worker, db, name, rating, strength):
    db_worker.execute(
        "UPDATE players SET ai_rating = ?, ai_strength = ? WHERE name = ?",
        (rating, strength, name)
    )

    db.commit()

    
client = OpenAI()

db = sqlite3.connect("player_database.db")
db_worker = db.cursor()

player_name = input("Enter player name: ").strip()

db_worker.execute(
    "SELECT * FROM players WHERE LOWER(name) = LOWER(?)",
    (player_name,)
)
players = db_worker.fetchall()

if not players:
    print("Player not found.")
    db.close()
    exit()

for player_data in players:
    name = player_data[0]
    position = player_data[1]
    club = player_data[2]
    goals = player_data[3]
    assists = player_data[4]


    try:
        analysis = analyze_player(client, name, position, club, goals, assists)
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        break

    print("\n--- AI SCOUT REPORT ---")
    print(f"Position: {position}")
    print(f"Club: {club}")
    print(f"Goals: {goals}")
    print(f"Assists: {assists}")
    print(f"Player: {analysis.player}")
    print(f"Rating: {analysis.rating}/10")
    print(f"Main strength: {analysis.strength}")

    save_analysis(db_worker, db, name, analysis.rating, analysis.strength)

    db_worker.execute(
    "SELECT name, ai_rating, ai_strength FROM players WHERE name = ?",
    (name,)
    )

    saved_player = db_worker.fetchone()
    print(f"Saved to database: {saved_player}")

db.close()