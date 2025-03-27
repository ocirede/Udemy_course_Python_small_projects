from turtle import Turtle

from setuptools.command.alias import alias

FONT = ("Courier", 24, "normal")
LEFT_ALIGNED = "left"
CENTER_ALIGNED = "center"

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.penup()
        self.color("black")
        self.hideturtle()
        self.goto(-280, 250)
        self.update_level()

    def update_level(self):
        self.clear()
        self.write(f"Level:{self.level}", False, align=LEFT_ALIGNED, font=FONT)

    def increase_level(self):
        self.level += 1
        self.clear()
        self.write(f"Level:{self.level}", False, align=LEFT_ALIGNED, font=FONT)

    def game_over(self):
        self.clear()
        self.goto(0, 0)
        self.write("Game Over", False, align=CENTER_ALIGNED, font=FONT)

