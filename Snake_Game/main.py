import time
from turtle import Screen
from snake import  Snake
from food import Food
from scoreboard import Scoreboard


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My snake game")
screen.tracer(0)
screen.listen()

snake = Snake()
food = Food()
score = Scoreboard()

screen.onkey(snake.go_up, "Up")
screen.onkey(snake.go_down, "Down")
screen.onkey(snake.go_left, "Left")
screen.onkey(snake.go_right, "Right")


game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()
    if snake.head.distance(food) < 15:
        food.refresh()
        score.increase_score()
        snake.add_new_segment()
    if snake.head.xcor() > 290 or snake.head.xcor()  < -290 or snake.head.ycor()  > 290 or snake.head.ycor() < -290:
        game_is_on = False
        score.game_over()
    elif snake.snake_death():
        game_is_on = False
        score.game_over()



screen.exitonclick()