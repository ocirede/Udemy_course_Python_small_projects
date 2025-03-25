import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

array_of_choices = [rock, paper, scissors]

my_score = 0
computer_score = 0

while my_score < 3 and computer_score < 3:
    my_choice_made = int(input("What do you choose? Type 0 for Rock, 1 for Paper, and 2 for Scissors: "))

    if my_choice_made not in [0, 1, 2]:
        print("Invalid choice! Please choose 0, 1, or 2.")
        continue

    print("\nYou chose:")
    print(array_of_choices[my_choice_made])

    computer_choice_made = random.randint(0, 2)

    print("Computer chose:")
    print(array_of_choices[computer_choice_made])

    if my_choice_made == computer_choice_made:
        print("It's a draw!")
    elif (my_choice_made == 0 and computer_choice_made == 2) or \
         (my_choice_made == 1 and computer_choice_made == 0) or \
         (my_choice_made == 2 and computer_choice_made == 1):
        print("You win this round!")
        my_score += 1
    else:
        print("Computer wins this round!")
        computer_score += 1

    print(f"Score -> You: {my_score}, Computer: {computer_score}\n")

if my_score == 3:
    print("Congratulations! You won the game! ")
else:
    print("Computer wins the game! Try again!")
