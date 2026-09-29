from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class PlayerAnalysis(BaseModel):
    player: str
    rating: int
    strength: str


player = input("Player name: ")
goals = int(input("Goals: "))
assists = int(input("Assists: "))


response = client.responses.parse(
    model="gpt-5.4-mini",
    input=f"""
Analyze this football player using the supplied stats.

Player: {player}
Goals: {goals}
Assists: {assists}

Give the player a rating from 1 to 10 and identify one main strength.
""",
    text_format=PlayerAnalysis
)


analysis = response.output_parsed

print("\n--- AI PLAYER ANALYSIS ---")
print(f"Player: {analysis.player}")
print(f"Rating: {analysis.rating}/10")
print(f"Main strength: {analysis.strength}")