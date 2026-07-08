from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 15, "normal")

class ScoreBoard(Turtle):
	def __init__(self):
		super().__init__()
		self.hideturtle()
		self.teleport(y=270, x=0)
		self.score = 0
		with open("data.txt", mode="r") as file:
			data = int(file.read())
		self.highscore = data
		self.color("white")
		self.penup()
		self.update_scoreboard()

	def update_scoreboard(self):
		self.clear()
		self.write(f"Score: {self.score} High Score: {self.highscore}", align=ALIGNMENT, font=FONT)

	def reset(self):
		if self.score > self.highscore:
			self.highscore = self.score
			with open("data.txt", mode="w") as file:
				file.write(str(self.highscore))
		self.score = 0
		self.update_scoreboard()

	# def game_over(self):
	# 	self.teleport(y=0, x=0)
	# 	self.color("red")
	# 	self.write(f"Game Over!", align=ALIGNMENT, font=FONT)

	def increase_score(self):
		self.score += 1
		self.clear()
		self.update_scoreboard()