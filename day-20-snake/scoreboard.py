from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 15, "normal")

class ScoreBoard(Turtle):
	def __init__(self):
		super().__init__()
		self.hideturtle()
		self.teleport(y=270, x=0)
		self.score = 0
		self.color("white")
		self.penup()
		self.update_scoreboard()

	def update_scoreboard(self):
		self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

	def game_over(self):
		self.teleport(y=0, x=0)
		self.color("red")
		self.write(f"Game Over!", align=ALIGNMENT, font=FONT)

	def increase_score(self):
		self.score += 1
		self.clear()
		self.update_scoreboard()