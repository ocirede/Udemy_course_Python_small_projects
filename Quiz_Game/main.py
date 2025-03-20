from  question_model import  Question
from data import  question_data
from quiz_brain import QuizBrain
question_Bank = []

for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_Bank.append(new_question)

quiz = QuizBrain(question_Bank)

while quiz.still_has_questions():
    quiz.next_question()
    print("\n")

print("You have completed the quiz")
print(f"Your final score was {quiz.score}/{quiz.question_number}")
