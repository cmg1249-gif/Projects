from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, coords):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.shapesize(stretch_wid=5, stretch_len=1)
        x = coords[0]
        y = coords[1]
        self.goto(x, y)

    def go_up(self):
        new_y = self.ycor() + 20
        if  self.ycor() > 250:
            pass
        else:
            self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - 20
        if self.ycor() < -225:
            pass
        else:
            self.goto(self.xcor(), new_y)