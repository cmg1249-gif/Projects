import random
tim = Turtle()
t.colormode(255)

tim.speed(0)

tim.pensize(1)

def random_color():
	r = random.randint(0,255)
	g = random.randint(0,255)
	b = random.randint(0,255)

	return r, g, b

def random_walk():
	for i in range(200):
		tim.color(random_color())
		angle = [0, 90, 180, 270]
		tim.fd(30)
		tim.seth(random.choice(angle))

def draw_spirograph(size_of_gap):
	for i in range(int(360 / size_of_gap)):
		tim.color(random_color())
		tim.circle(100)
		tim.seth(tim.heading() + size_of_gap)

draw_spirograph(10)


screen = Screen()
screen.exitonclick()