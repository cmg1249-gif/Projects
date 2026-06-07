from art import logo
import random
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
game_continues = True

def deal_card():
	return random.choice(cards)
def calculate_score(hand):
	score = sum(hand)
	if score == 21  and len(hand) == 2:
		return 0
	elif score > 21:
		for card in hand:
			if card == 11 and score > 21:
				score -= 10
	return score
user_cards = [deal_card(), deal_card()]
computer_cards = [deal_card(), deal_card()]

user_score = calculate_score(user_cards)
computer_score = calculate_score(computer_cards)

def compare(user_score1, computer_score1):
	if computer_score1 > 21:
		print("You Win!")
	elif computer_score1 > user_score1:
		print("You Lose!")
	elif computer_score1 == user_score1:
		print("Draw")
	else:
		print("You Win!")


while game_continues:
	if user_score == 0 or computer_score == 0:
		if computer_score == 0:
			print("Computer wins!")
			game_continues = False
		elif user_score == 0:
			print("User wins!")
			game_continues = False
	elif user_score > 21:
		print("You Lose!")
		game_continues = False
	else:
		another_card = input("Do you want to draw another card? (y/n): ").lower()
		if another_card == "y":
			user_cards.append(deal_card())
			user_score = calculate_score(user_cards)
			game_over = True
		else:
			game_continues = False
			compare(user_score, computer_score)
while computer_score < 17 and not game_over:
	computer_cards.append(deal_card())
	computer_score = calculate_score(computer_cards)
if not game_over:
	compare(user_score, computer_score)
