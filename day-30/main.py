# try:
# 	file = open("a_file.txt")
# 	a_dictionary = {"key": "value"}
# 	print(a_dictionary["key"])
# except FileNotFoundError:
# 	file = open("a_file.txt", "w")
# 	file.write("text")
# except KeyError as error_message:
# 	print(f"The key {error_message} does not exist")
# else:
# 	content = file.read()
# 	print(content)
# finally:
# 	raise KeyError("I made up this error")

#key error
# a_dictionary = {"key":"value"}
# value = a_dictionary["non_existing_key"]

#Index Error
# fruit_list = ["apple", "banana", "orange"]
# fruit = fruit_list[3]

# TypeError
# text = "abc"
# print(text + 5)

height = float(input("Height: "))
weight = float(input("Weight: "))

if height > 3:
	raise ValueError("Human height should not be over 3 meters")

bmi = weight / height ** 2

print(bmi)
