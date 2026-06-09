from art import logo
import random
GAME_OVER = False


print(logo)
print("Welcome to the Number Guessing Game!\n")
print("I'm thinking of a number between 1 and 100.\n")
lives = 0
MAGIC_NUMBER = random.randint(1, 100)

difficulty = input("Please choose a difficulty level. Type 'hard' or 'easy' ").lower()

if difficulty == "hard":
	lives = 5
elif difficulty == "easy":
	lives = 10
else:
	print("Sorry, you have to choose a difficulty level.")

def show_lives():
	"""Prints out the lives remaining of the game"""
	print(f"You have {lives} lives remaining.")

def players_guess():
	"""Takes players guess as input and converts it to an integer"""
	guess = int(input("Guess a number between 1 and 100: "))
	return guess
def check_guess(life, guess):
	"""Checks if the player guessed correctly, to low or high. Then updates the life variable if needed. Takes in Lives and Guess as input, returns game over or life reduction."""
	if guess == MAGIC_NUMBER:
		return life , True
	elif guess > MAGIC_NUMBER:
		print("Too high!")
		return life - 1 , False
	else:
		print("Too low!")
		return life - 1 , False



while not GAME_OVER and lives > 0:
	show_lives()
	guess = players_guess()

	lives, GAME_OVER = check_guess(lives, guess)

if lives == 0:
	print("You lose!")
else:
	print("You win!")
  
