from turtle import Screen, Turtle
from paddle import Paddle
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle(350, 0)


screen.listen()
screen.onkey(key="Up", fun=r_paddle.go_up())
screen.onkey(key="Down", fun=r_paddle.go_down)


game_is_on = True
while game_is_on:
    screen.update()





screen.exitonclick()