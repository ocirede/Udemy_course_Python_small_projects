from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10

class CarManager:
    def __init__(self):
        self.cars = []
        self.car_speed = STARTING_MOVE_DISTANCE


    def create_car(self):
        if random.randint(1, 6) == 1:
            new_car  = Turtle()
            new_car.shape("square")
            new_car.penup()
            new_car.color(random.choice(COLORS))
            new_car.turtlesize(stretch_wid=1, stretch_len=2)
            random_y_coordinate = random.randint(-250, 250)
            new_car.goto(300,  random_y_coordinate)
            new_car.setheading(180)
            self.cars.append(new_car)

    def cars_move(self):
        for car in self.cars:
            car.forward(self.car_speed)

    def increase_speed(self):
            self.car_speed += MOVE_INCREMENT

    def turtle_accident(self, player):
        for car in self.cars:
            if car.distance(player) < 20:
                return True



