squad = [
    {"name": "Haaland", "goals": 8},
    {"name": "Foden", "goals": 4},
    {"name": "Doku", "goals": 2}
]

def squad_report(squad):
    for player in squad:
        print(f"{player['name']} has {player['goals']} goals.")

        if player["goals"] >= 5:
            print("Elite Goal Scorer!") 
        
        else:
             print("Keep improving.")

squad[0]["goals"] = squad[0]["goals"] + 2


squad_report(squad)