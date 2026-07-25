from tkinter import *
from tkinter import messagebox

import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
FRA = "French"
ENG = "English"
card_info = ""


#------------------------- Picking Random Word for the Next Card --------------#
try:
	df = pandas.read_csv("./data/words_to_learn.csv")
	df_records = df.to_dict(orient="records")
except FileNotFoundError:
	df = pandas.read_csv("./data/french_words.csv")
	df_records = df.to_dict(orient="records")

def next_card():
	global card_info , flip_timer
	window.after_cancel(flip_timer)
	canvas.itemconfig(card_canvas, image=card_front_img)

	card_info = random.choice(df_records)
	ran_fra_word = card_info[FRA]
	canvas.itemconfig(title_text, text=FRA, fill="black")
	canvas.itemconfig(french_word, text=ran_fra_word, fill="black")
	flip_timer = window.after(3000, flip_card)


def flip_card():
	global card_info
	eng_word = card_info[ENG]
	canvas.itemconfig(card_canvas, image=card_back_img)
	canvas.itemconfig(title_text, text=ENG, fill="white")
	canvas.itemconfig(french_word, text=eng_word, fill="white")

def is_known():
	global card_info
	try:
		df_records.remove(card_info)
		data = pandas.DataFrame(df_records)
		data.to_csv("./data/words_to_learn.csv", index=False)
		next_card()
	except ValueError:
		messagebox.showerror("You Won!", "You learned all the words!")

#-------------------------- UI ------------------------#
# Window Creation
window = Tk()
window.title("Flashy")
window.configure(background=BACKGROUND_COLOR, padx=50, pady=50)
window.minsize(900, 800)

flip_timer = window.after(3000, flip_card)

# Canvas Creation
canvas = Canvas(width=850, height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_canvas = canvas.create_image(425, 300, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
# French Text
title_text = canvas.create_text(400,150,text="", font=("Ariel",40,"italic"))

# Word Text
french_word = canvas.create_text(400,300,text="", font=("Ariel",60,"bold"))

# Button creation
right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")

right_button = Button(image=right_img, highlightthickness=0,command=is_known)
wrong_button = Button(image=wrong_img, highlightthickness=0,command=next_card)

right_button.grid(row=1, column=1)
wrong_button.grid(row=1, column=0)

next_card()
window.mainloop()