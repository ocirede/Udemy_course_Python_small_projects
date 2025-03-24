from turtle import Turtle

class Pitch(Turtle):
    def __init__(self):
        super().__init__()
        self.define_pitch()


    def define_pitch(self):
        self.shape("square")
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 300)
        self.create_pitch()


    def create_pitch(self):
        length_pitch = 600 / 20
        self.setheading(270)
        for i in range(int(length_pitch)):
            self.pendown()
            self.forward(20)
            self.penup()
            self.forward(10)




