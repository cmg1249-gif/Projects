from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

def move_forwards():
    tim.forward(10)
def move_back():
    tim.backward(10)
def turn_left():
    tim.left(10)
def turn_right():
    tim.right(10)
def clear():
    tim.clear()
    tim.teleport(0,0)
    tim.setheading(0)
screen.listen()
screen.onkey(key="c", fun=clear)
screen.onkey(key="w", fun=move_forwards)
screen.onkey(key="Up", fun=move_forwards)
screen.onkey(key="s", fun=move_back)
screen.onkey(key="Down", fun=move_back)
screen.onkey(key="a", fun=turn_left)
screen.onkey(key="Left", fun=turn_left)
screen.onkey(key="d", fun=turn_right)
screen.onkey(key="Right", fun=turn_right)

screen.exitonclick()
