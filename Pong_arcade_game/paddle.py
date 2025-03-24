from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.create_paddle(position)

    def create_paddle(self, position):
        self.shape("square")
        self.color("white")
        self.penup()
        self.turtlesize(stretch_wid=5, stretch_len=1)
        self.setpos(position)

    def go_up(self):
        y_position = self.ycor()
        if y_position < 230:
            new_y_position = y_position + 20
            self.goto(self.xcor(), new_y_position)

    def go_down(self):
        y_position = self.ycor()
        if y_position > -230:
            new_y_position = y_position - 20
            self.goto(self.xcor(), new_y_position)



