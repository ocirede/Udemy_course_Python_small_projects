from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.create_the_ball()
        self.dx = 10
        self.dy = 10

    def create_the_ball(self):
        self.shape("circle")
        self.color("white")
        self.setpos(0, 0)
        self.penup()

    def ball_move(self):
        new_x = self.xcor() + self.dx
        new_y = self.ycor()+ self.dy
        self.goto(new_x, new_y)

    def bounce(self):
        if self.ycor() >= 290 or self.ycor() <= -290:
           self.dy *= -1

    def paddle_bounce(self, paddle):
        current_x_pos = self.xcor()
        if self.distance(paddle) < 50 and current_x_pos > 320 or  self.distance(paddle) < 50 and current_x_pos < -320:
            self.dx *= -1

    def right_score(self):
        curr_x_pos = self.xcor()
        if curr_x_pos > 400:
            return True

    def left_score(self):
        curr_x_pos = self.xcor()
        if curr_x_pos < -400:
            return True

    def reset_position(self):
        self.goto(0, 0)
        self.dx *= -1













