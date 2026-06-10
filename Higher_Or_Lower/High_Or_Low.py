#Import random, game_data and art modules
import random
import game_data
import art
game_continues = True
score = 0
# Display the logoo
print(art.logo)
# Choose contestants A and B randomly
def choose_ab():
	"""Randomly choosing contestants from game_data and prints their name country and description"""
	a_dictionary = random.choice(game_data.data)
	b_dictionary = random.choice(game_data.data)
	print(f"Compare A: {a_dictionary['name']}, a {a_dictionary['description']} from {a_dictionary['country']}\n")
	print(art.vs + "\n")
	print(f"Compare B: {b_dictionary['name']}, a {b_dictionary['description']} from {b_dictionary['country']}\n")
	return a_dictionary, b_dictionary

# Ask user who has more fallowers A or B

def ask_user():
	"""Asks the user to guess who has more fallowers"""
	player_guess = input("Who has more followers? 'A' or 'B': ").lower()
	return player_guess

#Check if user is correct. If no game ends if yes continue
def check(guess,a_fallowers,b_fallowers):
	"""Checks if the users answer was correct. Returns true or false"""
	if guess == "a" and a_fallowers > b_fallowers or guess == "b" and b_fallowers > a_fallowers:
		return True
	else:
		return False
# User is correct. Previous 'B' becomes 'A' and a new 'B' is randomly chosen
## Update and display the score and game continues
def new_contestants(contest_b, f_score):
	"""Changes B to A and adds new contestant to B."""
	contestant_a = contest_b
	new_score = f_score + 1
	contestant_b = random.choice(game_data.data)
	print(art.logo)
	print(f"Compare A: {contestant_a['name']}, a {contestant_a['description']} from {contestant_a['country']}\n")
	print(art.vs + "\n")
	print(f"Compare B: {contestant_b['name']}, a {contestant_b['description']} from {contestant_b['country']}\n")
	return contestant_a, contestant_b, new_score


dictionary_a, dictionary_b = choose_ab()

while game_continues:
	user_guess = ask_user()
	if not check(user_guess,dictionary_a["follower_count"],dictionary_b["follower_count"]):
		print("You LOSE!")
		game_continues = False
	else:
		dictionary_a, dictionary_b, score = new_contestants(dictionary_b, score)
		print(f"Your score is {score}")
    
