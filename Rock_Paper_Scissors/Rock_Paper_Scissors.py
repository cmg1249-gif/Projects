import random


rock = ''' rock
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = ''' paper
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = ''' scissors
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''


# Human Input
try:
    player_roll = int(input("What do you choose? Type 0 for Rock, 1 for Paper, 2 for Scissors: "))
except ValueError:
    print("Please enter a whole number 0-2")
if player_roll > 2 or player_roll < 0:
    print("Invalid input, please try again")
else:
    rock_paper_scissors = [rock,paper,scissors]
    player_choice = rock_paper_scissors[player_roll]

    print("Player chose: " + player_choice)

# Computer choice
    computer_choice = random.choice(rock_paper_scissors)
    print("Computer chose: " + computer_choice)

if player_choice == computer_choice:
    print("Draw")
elif player_choice == rock and computer_choice == paper:
    print("You Lose!")
elif player_choice == rock and computer_choice == scissors:
    print("You Win!")
elif player_choice == scissors and computer_choice == rock:
    print("You Lose!")
elif player_choice == scissors and computer_choice == paper:
    print("You Win!")
elif player_choice == paper and computer_choice == rock:
    print("You Win")
elif player_choice == paper and computer_choice == scissors:
    print("You Lose!")
