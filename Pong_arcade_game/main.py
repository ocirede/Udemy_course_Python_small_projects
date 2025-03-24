from turtle import  Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from pitch import Pitch
import time


screen = Screen()
screen.tracer(0)
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong game")

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))

ball = Ball()
pitch = Pitch()
pitch.create_pitch()
score_l = Scoreboard((- 35, 230 ))
score_r = Scoreboard((35, 230 ))

screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")

screen.onkey(l_paddle.go_up, "u")
screen.onkey(l_paddle.go_down, "d")

game_is_on = True

while game_is_on:
    time.sleep(0.06)
    screen.update()
    ball.ball_move()
    ball.bounce()
    ball.paddle_bounce(r_paddle)
    ball.paddle_bounce(l_paddle)
    if ball.right_score():
        score_l.increase_score()
        ball.reset_position()
    elif ball.left_score():
        score_r.increase_score()
        ball.reset_position()




screen.exitonclick()