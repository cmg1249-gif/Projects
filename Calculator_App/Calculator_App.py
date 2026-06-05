from art import logo
print(logo)
def add(n1, n2):
    return n1 + n2

# TODO: Write out the other 3 functions - subtract, multiply, divide.

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

# TODO: Add these 4 functions into a dictionary as the values. Keys = "+", "-", "*", "/"
operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}
# TODO: Use the dictionary operations to perform the calculations. Multiply 4 * 8 using the dictionary.

perform_multiply = operations["*"]
perform_add = operations["+"]
perform_subtract = operations["-"]
perform_divide = operations["/"]
will_continue = True
first_number = int(input("Enter a number: "))
while will_continue:
    operator = input("What' the operator?: ")
    second_number = int(input("What' the next number?: "))
    user_continue = input("Would you like to continue with another number?(y/n)?: ").lower()

    if operator == "+":
        result = perform_add(first_number, second_number)
        print(f"{first_number} + {second_number} = {result}")
    elif operator == "-":
        result = perform_subtract(first_number, second_number)
        print(f"{first_number} - {second_number} = {result}")
    elif operator == "*":
        result = perform_multiply(first_number, second_number)
        print(f"{first_number} * {second_number} = {result}")
    elif operator == "/":
        result = divide(first_number, second_number)
        print(f"{first_number} / {second_number} = {result}")
    else:
        print("Sorry, I didn't understand.")
    if user_continue != "y":
        will_continue = False
    first_number = result
