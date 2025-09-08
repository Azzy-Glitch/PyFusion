import random

Computer = random.choice([-1, 0, 1])
Playerstr = input("Enter Player choice: ")
PlayerDict = {"s": 1, "w": -1, "g": 0}
reverseDict = {1: "Snake", -1: "Water", 0: "Gun"}

Player = PlayerDict[Playerstr]

print(f"Player chose {reverseDict[Player]}\nComputer chose {reverseDict[Computer]}")

if(Computer == Player):
    print("Its a draw")

else:
   
   if (Player == 1 and Computer == -1) or \
   (Player == -1 and Computer == 0) or \
   (Player == 0 and Computer == 1):
    print("Player Win!")
   else:
    print("Player Lose!")
