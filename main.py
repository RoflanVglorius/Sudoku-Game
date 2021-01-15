import game
import pickle
import os

while True:
    print("Choose game mode: 0 - computer/1 - human")
    mode = int(input())
    if mode == 1:
        print("Would you like to load game? Y/N")
        answer = input()
        if answer == "Y":
            print("Enter filename: ")
            with open(input(), "rb") as file:
                g = pickle.load(file)
            g.play(1)
            exit(0)
    print("Enter amount of filled cells: ")
    amount = int(input())
    g = game.Game(amount)
    g.play(mode)
    print("Would you like to start a new game? Y/N")
    answer = input()
    if answer == "N":
        break
    os.system('cls' if os.name == 'nt' else 'clear')
