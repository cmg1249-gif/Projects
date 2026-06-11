MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}
game_continues = True
profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

def ask_user():
    """Asks the user for their order from the menu"""
    user_answer = input("What would you like? (espresso/latte/cappuccino): ")
    return user_answer

def check_choice(a_user_choice):
    if a_user_choice == "report":
        print(f"Water: {resources["water"]}ml\nMilk: {resources["milk"]}ml\nCoffee: {resources["coffee"]}g\nMoney: ${profit:.2f}")
        return True
    elif a_user_choice == "off":
        return False
    else:
        return True

def check_ingredients(menu_drink_ingredients):
    for item in menu_drink_ingredients:
        if menu_drink_ingredients[item] > resources[item]:
            print(f"not enough {item} to make a drink.")
            return False
    else:
        return True

def calculate():
    quarters = int(input("How many Quarters: ")) * 0.25
    dimes = int(input("How many Dimes: ")) * 0.10
    nickles = int(input("How many Nickles: ")) * 0.05
    pennys = int(input("How many Pennys: ")) * 0.01
    sum =  quarters + dimes + nickles + pennys
    return sum
def compare_cost(coffee_cost, money_provided):
    if coffee_cost > money_provided:
        return False
    else:
        return True

def deal_change(coffee_cost, money_provided):
    change = money_provided - coffee_cost
    money_made = coffee_cost + profit
    return change, money_made

def make_drink(user_choice):
    user_ingredients = MENU[user_choice]["ingredients"]
    for item in user_ingredients:
        resources[item] -= user_ingredients[item]
    print(f"Enjoy your {user_choice}! ")
enough_ingredients = True
while game_continues:
    user_choice = ask_user()
    if user_choice == "off":
        game_continues = check_choice(user_choice)
    elif user_choice == "report":
        check_choice(user_choice)
        continue
    else:
        if not check_ingredients(MENU[user_choice]["ingredients"]):
            print(f"Sorry, {user_choice} is not enough ingredients to make a drink.")
            continue
        coins = calculate()
        if compare_cost( MENU[user_choice]["cost"], coins):
            change, money_made = deal_change(MENU[user_choice]["cost"], coins)
            profit = money_made
            print(f"Your change is ${change:.2f}")
            make_drink(user_choice)
            continue
          
