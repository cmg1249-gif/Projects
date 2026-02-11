import sys
#Password Security Score Calculator
user_passwd = input("Enter your password for a Security Score!:")
# Setting some possible variables I may use in the future
#User password varialbles


user_passwd_length = len(user_passwd)


#Scoring variables

#Password length score

if user_passwd_length <= 6:
    score_length = 0
elif 7 <= user_passwd_length <= 11:
    score_length = 2
elif user_passwd_length >= 12:
    score_length = 2.5

    
print("Lenght Score:", score_length)

#Password special character score
special_count = 0
for char in user_passwd:
    if char in "!@#$%^&*()-_=+[]{}|;:,.<>?":
        special_count += 1

if special_count <= 1:
    score_sc = 0
elif 2 <= special_count <= 3:
    score_sc = 2
elif special_count >= 4:
    score_sc = 2.5

print("Special Character Score:", score_sc)


#Password Number score
passwd_numbers = sum(1 for char in user_passwd if char.isdigit())

if passwd_numbers <=1:
    score_numbers = 0
elif 2 <= passwd_numbers <= 3:
    score_numbers = 2
elif passwd_numbers >= 4:
    score_numbers = 2.5

print("Number Score:", score_numbers)
      
      #Lenth Score
passwd_upper = any(char.isupper() for char in user_passwd)
if passwd_upper == True:
    score_upper = 2
else:
    score_upper = 0 
print("Upper Score Score:", score_upper)
# Path to the wordlist goes here
with open("C:\\Users\\Connor Glasner\\Documents\\rockyou\\rockyou.txt", "r", encoding="latin-1") as file:
    wordlist = file.read().splitlines()

    if user_passwd in wordlist:
        Final_score = 0
        print("Password is in the wordlist:")
        sys.exit()
    else:
        ry_score = 2.5
        print("Password is not in the wordlist:")


#Final Score Calculation
user_passwd_score = score_length + score_sc + score_numbers + score_upper
print(f"Your password score is: {user_passwd_score}/12")
      
percentage_score = round((user_passwd_score / 12) * 100, 2)
print(f"Your password score is: {percentage_score}%")


