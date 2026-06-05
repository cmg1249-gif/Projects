def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

# TODO: Add these 4 functions into a dictionary as the values. Keys = "+", "-", "*", "/"

# TODO: Use the dictionary operations to perform the calculations. Multiply 4 * 8 using the dictionary.
def calculator():
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    will_continue = True
    first_number = int(input("Enter a number: "))
    while will_continue:
        operator = input("What' the operator?: ")
        second_number = int(input("What' the next number?: "))
        user_continue = input("Would you like to continue with another number?(y/n)?: ").lower()

        if operator == "+":
            result = operations["+"](first_number, second_number)
            print(f"{first_number} + {second_number} = {result}")
        elif operator == "-":
            result = operations["-"](first_number, second_number)
            print(f"{first_number} - {second_number} = {result}")
        elif operator == "*":
            result = operations["*"](first_number, second_number)
            print(f"{first_number} * {second_number} = {result}")
        elif operator == "/":
            result = operations["/"](first_number, second_number)
            print(f"{first_number} / {second_number} = {result}")
        else:
            print("Sorry, I didn't understand.")
        if user_continue != "y":
            will_continue = False
            print("\n" * 20)
        calculator()
        first_number = result
calculator()
