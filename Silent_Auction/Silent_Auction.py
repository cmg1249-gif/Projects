from art import logo

print(logo)
name = input("What is your name?")
price = int(input("How much would you like to bid? $"))

bid_dictionary = {}
bid_dictionary[name] = price

new_bid_q = input("Will there be any more bides? Type exactly 'yes' or 'no'")
while new_bid_q == "yes":
	print("\n" * 100)
	name = input("What is your name?")
	price = int(input("How much would you like to bid? $"))
	bid_dictionary[name] = price
	new_bid_q = input("Will there be any more bides? Type exactly 'yes' or 'no'")
bid_size = 0
bid_winner = ""
for key in bid_dictionary:
	if bid_dictionary[key] > bid_size:
		bid_size = bid_dictionary[key]
		bid_winner = key
print(f"{bid_winner} is the winner! With a bid of ${bid_size}.")
