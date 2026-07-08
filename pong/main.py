from turtle import Screen
from paddle import Paddle
from ball import Ball
import time
from scoreboard import Scoreboard
R_PADDLE = (350, 0)
L_PADDLE = (-350, 0)

# Screen configuration
screen = Screen()
screen.setup(width=800, height=600)
screen.tracer(0)
screen.bgcolor("black")
screen.title("Pizzong")
screen.listen()

# Creation of paddles form the Paddle class
r_paddle = Paddle(R_PADDLE)
l_paddle = Paddle(L_PADDLE)
ball = Ball()
scoreboard = Scoreboard()
# Right paddle listening for user input
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")

# Left paddle listening for user input

screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")







game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()
    # Detect collision w/ wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision w/ right paddle
    if  ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()



    # Detect R paddle miss
    if ball.xcor() > 380:
        ball.reset()
        scoreboard.l_point()

    #Detect L paddle miss
    if ball.xcor() < -380:
        ball.reset()
        scoreboard.r_point()

screen.exitonclick()