from turtle import Turtle
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.create_turtle()

    def create_turtle(self):
        self.shape("turtle")
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(90)

    def turtle_move(self):
        self.forward(MOVE_DISTANCE)


    def end_race(self):
        curr_y_pos = self.ycor()
        if curr_y_pos == FINISH_LINE_Y:
           return True

    def reset_position(self):
        self.goto(STARTING_POSITION)



