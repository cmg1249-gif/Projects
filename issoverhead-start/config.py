import string
import secrets

ascii: list = [letter for letter in string.ascii_letters]
digits: list = [letter for letter in string.digits]
punctuation: list = [letter for letter in string.punctuation]
new_pw: list = []
for _ in range(7):
	new_pw.append(secrets.choice(ascii))
for _ in range(5):
	new_pw.append(secrets.choice(digits))
for _ in range(3):
	new_pw.append(secrets.choice(punctuation))


def secure_shuffle(items: list) -> None:
	"""Shuffle a list in place using cryptographically secure random order"""
	for i in range(len(items) - 1, 0, -1):
		j = secrets.randbelow(i + 1)
		items[i], items[j] = items[j], items[i]

secure_shuffle(new_pw)
new_pw = ''.join(new_pw)
print(new_pw)

