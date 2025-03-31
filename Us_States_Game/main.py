import pandas as pd
import turtle

screen = turtle.Screen()
screen.title("Us States game")
image = "blank_states_img.gif"
screen.setup(width=800, height=800)

turtle.addshape(image)
turtle.shape(image)

data = pd.read_csv("50_states.csv")
list_states = data.state.tolist()
correct_states = []

def writing_state(x, y, state):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.write(f"{state}", False, align="center", font=("Arial", 10, "normal"))

while len(correct_states) < 50:
    answer_state = screen.textinput(title=f"{len(correct_states)}/50 correct States",
                                    prompt="What's another state's name?").title()

    if answer_state is None:
        continue

    check_state = data[data["state"] == answer_state]

    if not check_state.empty and answer_state not in correct_states:
        correct_states.append(answer_state)
        x_coordinate = float(check_state.x.iloc[0])
        y_coordinate = float(check_state.y.iloc[0])
        writing_state(x_coordinate, y_coordinate, answer_state)

    if answer_state == "Exit":
        missing_states = []
        for state in list_states:
            if state not in correct_states:
                missing_states.append(state)
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

screen.mainloop()