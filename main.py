import sqlite3
from openai import OpenAI
from pydantic import BaseModel, Field

class PlayerAnalysis(BaseModel):
    player: str
    rating: int = Field(ge=1, le=10)
    strength: str

    
client = OpenAI()

db = sqlite3.connect("player_database.db")
db_worker = db.cursor()



db_worker.execute("SELECT * FROM players")
players = db_worker.fetchall()


for player in players[:1]:
    name = player[0]
    position = player[1]
    club = player[2]
    goals = player[3]
    assists = player[4]


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

    analysis = response.output_parsed

    db_worker.execute(
    "UPDATE players SET ai_rating = ?, ai_strength = ? WHERE name = ?",
    (analysis.rating, analysis.strength, name)
)

    db.commit()

    print(f"Player: {analysis.player}")
    print(f"Rating: {analysis.rating}/10")
    print(f"Main strength: {analysis.strength}")

