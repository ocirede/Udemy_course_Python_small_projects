import pandas as pd
import turtle

screen = turtle.Screen()
screen.title("Us States game")
image = "blank_states_img.gif"
screen.setup(width=800, height=800)

turtle.addshape(image)
turtle.shape(image)

data = pd.read_csv("50_states.csv")
total_states = len(data)
correct_states = 0

def writing_state(x, y, state):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.write(f"{state}", False, align="center", font=("Arial", 10, "normal"))

def game_over():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.pendown()
    turtle.write(f"Congrats!! you have guessed all the {total_states} States", False, align="center",font=("Arial", 18, "normal"))


while correct_states < total_states:
    answer_state = screen.textinput(title=f"{correct_states}/{total_states} correct States", prompt="What's another State's name").title()
    check_state = data[data["state"] == answer_state]
    if check_state.empty or answer_state is None:
        continue
    elif check_state.state.iloc[0] == answer_state:
        correct_states += 1
    x_coordinate = float(check_state.x.iloc[0])
    y_coordinate = float(check_state.y.iloc[0])
    writing_state(x_coordinate, y_coordinate, answer_state)
game_over()

screen.mainloop()