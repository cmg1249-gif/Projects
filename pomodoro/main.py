from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 20
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 25
reps = 0
REPS_WORK_SEC = (1, 3, 5, 7)
REPS_LONG_BREAK_SEC = 8
REPS_SHORT_BREAK_SEC = (2, 4, 6)
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
	window.after_cancel(timer)
	label_timer.config(text="Timer",fg=GREEN,bg=YELLOW)
	label_checkm.config(text="",fg=PINK,bg=YELLOW)
	canvas.itemconfig(timer_text, text="00:00")
	global reps
	reps = 0
	global check_marks
	check_marks = []

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
	global reps
	reps += 1
	work_sec = WORK_MIN * 60
	short_break_sec = SHORT_BREAK_MIN * 60
	long_break_sec = LONG_BREAK_MIN * 60


	#If it's the 1st/3rd/5th/7th rep:
	if reps in REPS_WORK_SEC:
		count_down(work_sec)
		label_timer.config(text="Work",fg=GREEN,bg=YELLOW)
	#If it's the 8th rep:
	elif reps == REPS_LONG_BREAK_SEC:
		count_down(long_break_sec)
		label_timer.config(text="Break",fg=RED,bg=YELLOW)
	#If it's the 2nd/4th/6th
	elif reps in REPS_SHORT_BREAK_SEC:
		count_down(short_break_sec)
		label_timer.config(text="Break",fg=PINK,bg=YELLOW)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
check_marks = []
def count_down(count):

	count_min = math.floor(count / 60)
	count_sec = count % 60
	if count_sec < 10:
		count_sec = f"0{count_sec}"

	canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
	if count > 0:
		global timer
		timer = window.after(1000, count_down, count-1)
	else:
		start_timer()
		if reps % 2 == 0:
			check_marks.append("✔")
			check_mark_string = ''.join(check_marks)
			label_checkm.config(text=check_mark_string)


# ---------------------------- UI SETUP ------------------------------- #
# Window Creation
window = Tk()
window.title("Pomodoro")
window.configure(bg=YELLOW,padx=50,pady=50)

# Tomato Canvas Creation
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100,112, image=tomato_img)
timer_text = canvas.create_text(100,130, text ='00:00', fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1,row=1)

# Label and Button Creation
# Start Button
button_start = Button(text="Start",font=FONT_NAME,command=start_timer, width=6, height=1, highlightthickness=0)
button_start.grid(column=0,row=2)

# Reset Button
button_reset = Button(text="Reset",font=FONT_NAME, command = reset_timer, width=6, height=1, highlightthickness=0)
button_reset.grid(column=2,row=2)

# Timer Label
label_timer = Label(text="Timer",font=(FONT_NAME, 45, "bold"), bg=YELLOW,fg=GREEN)
label_timer.grid(column=1,row=0)

# Checkmark Label
label_checkm = Label(font=(FONT_NAME, 20, "bold"), bg=YELLOW,fg=GREEN)
label_checkm.grid(column=1, row=3)

window.mainloop()
