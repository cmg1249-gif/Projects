from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
import time
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake")
screen.tracer(0)


snake = Snake()
food = Food()
scoreboard = ScoreBoard()
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right,"Right")
game_is_on = True
while game_is_on:
	screen.update()
	time.sleep(0.1)
	snake.move()

	#Detect collision w/ food
	if snake.head.distance(food) < 17:
		food.refresh()
		snake.extend()
		scoreboard.increase_score()



	#Detect collision w/ wall
	if snake.head.xcor() > 299 or snake.head.xcor() < -299 or snake.head.ycor() > 299 or snake.head.ycor() < -299:
		scoreboard.reset()
		snake.reset()
	#Detect collision w/ tail
	for segment in snake.segments:
		if segment == snake.head:
			pass
		elif snake.head.distance(segment) < 10:
			scoreboard.reset()
			snake.reset()

screen.exitonclick()