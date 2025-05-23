import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
player = Player()
car = CarManager()
level = Scoreboard()
screen.onkey(player.turtle_move, "Up")
screen.listen()
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car.create_car()
    car.cars_move()
    if player.end_race():
         level.increase_level()
         player.reset_position()
         car.increase_speed()
    if car.turtle_accident(player):
        level.game_over()
        game_is_on = False

screen.exitonclick()

