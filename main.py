name = input("Player Name: ")

try:
    goals = int(input("Goals: "))

except ValueError:
    print("Please enter a valid number.")
    exit()


player = {
    "name": name,
    "goals": goals
}


import json

file = open("player.json", "w")

json.dump(player, file)

file.close()

opened_file = open("player.json", "r")

saved_player = json.load(opened_file)

opened_file.close()

print(saved_player)

def check_player(player):


    if player["goals"] >= 5:
     return"Elite GoalScorer!"

    else:
     return"Keep improving."

print(check_player(saved_player))

