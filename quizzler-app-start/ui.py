from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:

	def __init__(self,quiz_brain: QuizBrain):
		self.quiz = quiz_brain
		self.window = Tk()
		self.window.title("Quizzler")
		self.window.config(padx=20, pady=20, bg=THEME_COLOR)
		self.window.minsize(300, 400)

		#Canvas
		self.canvas = Canvas(self.window,width=300,height=250, bg="white")
		self.id = self.canvas.create_text(150,125,font=("Arial",20,"italic"), width=280)
		self.canvas.itemconfig(self.id,text="")
		self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

		#Label
		self.score_label = Label(self.window, text=f"Score:{self.quiz.score}",padx=20,pady=20,
								 bg=THEME_COLOR, fg="white",font=("Arial",12,"bold"))
		self.score_label.grid(row=0, column=1, padx=20,pady=20)

		#Buttons
		img_button_t = PhotoImage(file="./images/true.png")
		img_button_f = PhotoImage(file="./images/false.png")
		self.button_t = Button(self.window, image=img_button_t, highlightthickness=0, command=self.true_pressed)
		self.button_f = Button(self.window, image=img_button_f, highlightthickness=0, command=self.false_pressed)
		self.button_t.grid(row=2, column=0,padx=20,pady=20)
		self.button_f.grid(row=2, column=1,padx=20,pady=20)
		self.get_next_question()


		self.window.mainloop()

	def get_next_question(self):
		self.change_white()
		if self.quiz.still_has_questions():
			self.score_label.config(text=f"Score:{self.quiz.score}/{self.quiz.question_number}")
			q_text = self.quiz.next_question()
			self.canvas.itemconfig(self.id,text=q_text)
		else:
			self.canvas.itemconfig(self.id,text="No questions left")
			self.button_t.config(state="disabled")
			self.button_f.config(state="disabled")

	def true_pressed(self):
		is_right = self.quiz.check_answer("True")
		self.give_feedback(is_right)

	def false_pressed(self):
		is_right = self.quiz.check_answer("False")
		self.give_feedback(is_right)

	def give_feedback(self, is_right):
		if is_right:
			self.change_green()
			self.window.after(1000, self.get_next_question)

		else:
			self.change_red()
			self.window.after(1000, self.get_next_question)

	def change_white(self):
		self.canvas.config(bg="White")


	def change_green(self):
			self.canvas.config(bg="Green")



	def change_red(self):
			self.canvas.configure(bg="Red")
