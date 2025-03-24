from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self, position):
        super().__init__()
        self.scoreboard(position)

    def scoreboard(self, position):
        self.score = 0
        self.penup()
        self.color("white")
        self.hideturtle()
        self.goto(position)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"{self.score}", False, align="center", font=("Arial", 48, "normal", ))

    def increase_score(self):
        self.score += 1
        self.update_score()

