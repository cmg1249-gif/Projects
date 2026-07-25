import smtplib
import os

my_email = os.environ["MY_EMAIL"]
password = os.environ["EMAIL_PASSWORD"]

#
# with smtplib.SMTP("smtp.gmail.com", 587) as connection:
# 	connection.starttls()
# 	connection.login(user=my_email, password=password)
# 	connection.sendmail(from_addr=my_email,to_addrs="you@example.com",
# 						msg="Subject:Hello\n\n This is the body of my email")
#

import datetime as dt
import random

now = dt.datetime.now()
year = now.year
month = now.month
day = now.day
day_of_week = now.weekday()



if day_of_week == 4:
	with open("quotes.txt", "r") as f:
		quotes = f.readlines()
		random_quote = random.choice(quotes)
	with smtplib.SMTP("smtp.gmail.com", 587) as connection:
		connection.starttls()
		connection.login(user=my_email, password=password)
		connection.sendmail(from_addr=my_email, to_addrs="you@example.com",
							msg=f"Subject:Happy Monday!\n\n{random_quote}")