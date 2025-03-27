
with open("Input/Letters/starting_letter.txt") as mail:
    mail_template = mail.read()

with open("Input/Names/invited_names.txt") as names:
    list_of_names = names.readlines()

for name in list_of_names:
    new_name = name.strip()
    personalized_mail = mail_template.replace("[name]", new_name)
    with open(f"./Output/ReadyToSend/letter_for_{new_name}.docx", mode="w") as saving_mails:
        saving_mails.write(personalized_mail)



