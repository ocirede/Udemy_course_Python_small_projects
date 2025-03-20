from turtle import Turtle

ALIGNMENT = "center"
FONT= ("Arial", 16, "normal", )
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.color("white")
        self.hideturtle()
        self.goto(0, 260)
        self.update_score()



    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score} ", False, align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.clear()
        self.write(f"Game Over ", False, align=ALIGNMENT, font=FONT)


    def increase_score(self):
        self.score += 1
        self.update_score()