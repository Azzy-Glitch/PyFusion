
import random
'''
1 for snake
-1 for water 
0 for gun

'''
Computer = random.choice([-1, 0, 1])
Playerstr = input("Enter Player choice: ")
PlayerDict = {"s": 1, "w": -1, "g": 0}
reverseDict = {1: "Snake", -1: "Water", 0: "Gun"}

Player = PlayerDict[Playerstr]

print(f"Player chose {reverseDict[Player]}\nComputer chose {reverseDict[Computer]}")

if(Computer == Player):
    print("Its a draw")

else:
    if(Computer ==-1 and Player == 1): 
        print("Player win!")

    elif(Computer ==-1 and Player == 0):
        print("Player Lose!")

    elif(Computer == 1 and Player == -1):
        print("Player lose!")

    elif(Computer ==1 and Player == 0):
        print("Player Win!")

    elif(Computer ==0 and Player == -1):
        print("Player Win!")

    elif(Computer == 0 and Player == 1):
        print("Player Lose!")

    else:
        print("Something went wrong!")
