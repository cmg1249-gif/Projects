import time
from turtle import Screen
from player import Player, FINISH_LINE_Y
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.creat_cars()
    car_manager.move_cars()
    # Detect Collision W/ a Car
    for car in car_manager.all_cars:
        if car.distance(player) < 24:
            game_is_on = False
            scoreboard.game_over()

    # Detect if player has reached the finish line
    if player.ycor() >= FINISH_LINE_Y:
        player.reset_player()
        car_manager.level_up()




screen.exitonclick()