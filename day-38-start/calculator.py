def add(a,b):
    return a+b

def sub(a,b):
	return a-b

if __name__ == "__main__":

	print("This is a simple calculator!")
	num1 = int(input("Enter a number: "))
	num2 = int(input("Enter another number: "))
	print(f"The sum is: {add(num1,num2)}")
	print(f"The difference is: {sub(num1,num2)}")

