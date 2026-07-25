##################### Extra Hard Starting Project ######################
import datetime as dt
import smtplib
import random
import pandas as pd

FILE_LIST = ["./letter_templates/letter_1.txt", "./letter_templates/letter_2.txt", "./letter_templates/letter_3.txt"]
my_email = "pythont271@gmail.com"
password = "temj lydx nkah atzu"
# 1. Update the birthdays.csv
now = dt.datetime.now()
month = now.month
day = now.day
# 2. Check if today matches a birthday in the birthdays.csv
df = pd.read_csv("birthdays.csv")
df_dict = df.to_dict(orient="records")

for d in df_dict:
	if d["month"] == month and d["day"] == day:
		recp_name = d["name"]
		recp_email = d["email"]

		# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
		random_letter = random.choice(FILE_LIST)
		with open(random_letter, "r") as f:
			file_string = f.read()
			file_string = file_string.replace("[NAME]", recp_name)

		# 4. Send the letter generated in step 3 to that person's email address.

		with smtplib.SMTP("smtp.gmail.com", 587) as connection:
			connection.starttls()
			connection.login(user=my_email, password=password)
			connection.sendmail(from_addr=my_email, to_addrs=recp_email,
			                    msg=f"Subject: Happy Birthday\n\n{file_string}")
