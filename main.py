name = input("Whats is your name? ")
print(f"welcome {name}!")

goals = int(input("How many goals have you scored? "))

assists = int(input("How many assists have you made? "))

if goals >= 2 and assists >= 1:

    print("Elite Performance")

else:

    print("Keep Improving")


players = ["Haaland", "Foden", "Doku", "Rodri"]


for player in players: 

    print(f" Checking {player}!") 

    if player is "Haaland":

        print("STAR PLAYER FOUND")

print(f"there are {len(players)} players in the squad")



def football_training():
    print("Training started!")
    print("Scanning...")
    print("Passing...")
    print("Training complete!")

football_training()
