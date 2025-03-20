import colorgram
from turtle import Turtle, Screen
import random


color_turtle = Turtle()
screen = Screen()
screen.colormode(255)
color_turtle.speed("fastest")
color_turtle.penup()
color_turtle.hideturtle()
color_list = [(235, 242, 249), (237, 224, 80), (205, 4, 73), (236, 50, 130), (198, 164, 8), (111, 179, 218),
              (204, 75, 12), (219, 161, 103), (234, 224, 4), (11, 23, 63), (29, 189, 111), (22, 107, 174),
              (16, 28, 177), (216, 134, 179), (8, 186, 216), (229, 167, 200), (210, 25, 148)]
color_turtle.setheading(225)
color_turtle.forward(300)
color_turtle.setheading(0)

number_of_dots = 100


for dot_count in range(1, number_of_dots + 1):
    random_colors = random.choice(color_list)
    color_turtle.dot(20, random_colors)
    color_turtle.forward(50)

    if dot_count % 10 == 0:
        color_turtle.setheading(90)
        color_turtle.forward(50)
        color_turtle.setheading(180)
        color_turtle.forward(500)
        color_turtle.setheading(0)








screen.exitonclick()


colors_tuples = []
colors_image = colorgram.extract("image.jpg", 20)
def replicate_colors(colors):
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        rgb = (r, g, b)
        colors_tuples.append(rgb)

replicate_colors(colors_image)