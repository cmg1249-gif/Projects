from turtle import Turtle, Screen
import random

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
turtles = []
is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: " )

for i in range(len(colors)):
	turtles.append(Turtle(shape="turtle"))
	turtles[i].color(colors[i])
	turtles[i].penup()
	turtles[i].goto(x=-230, y=i * 30 - 50)

if user_bet:
	is_race_on = True

while is_race_on:

	for turtle in turtles:
		if turtle.xcor() >= 230:
			is_race_on = False
			winning_color = turtle.pencolor()
			if winning_color == user_bet:
				print(f"You won the race! The winner is {winning_color}!")
			else:
				print(f"The winner is {winning_color}, You lost!")
		random_distance = random.randint(0,10)
		turtle.forward(random_distance)

screen.exitonclick()
