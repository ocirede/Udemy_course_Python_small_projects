from turtle import Turtle
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]


    def create_snake(self):
        for i in range(3):
            new_segment = Turtle(shape="square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(i * - 20, 0)
            self.segments.append(new_segment)
        return self.segments

    def add_new_segment(self):
        extra_segment = Turtle(shape="square")
        extra_segment.penup()
        extra_segment.color("white")
        last_segment = self.segments[-1]
        current_x_position = last_segment.xcor()
        current_y_position = last_segment.ycor()
        extra_segment.goto(current_x_position, current_y_position)
        self.segments.append(extra_segment)


    def move(self):
        for seg_num in range(len(self.segments) -1 , 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head .forward(MOVE_DISTANCE)


    def snake_death(self):
        for segment in self.segments[1:]:
            if self.head.distance(segment) < 5:
               return True


    def go_up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def go_down(self):
        if self.head.heading() != UP:
             self.head .setheading(DOWN)

    def go_left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def go_right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)


