import smtplib
import datetime as dt
import random
import pandas as pd
import os

#--------------CONSTANTS---------------#

TITLE_MAIL = "Happy Birthday"

#--------------DATETIME---------------#
now = dt.datetime.now()
day = now.day
month = now.month

#--------------READ CSV---------------#
birthdays = pd.read_csv("birthdays.csv")
dic_birthdays = birthdays.to_dict(orient="records")

#--------------OS FILE-PATH---------------#
folder_path = os.path.join("./letter_templates")
filenames = os.listdir(folder_path)
random_filename = random.choice(filenames)
file_path = os.path.join(folder_path, random_filename)

#--------------MAIN FUNCTIONALITY---------------#
for person in dic_birthdays:
    if person["month"] == month and person["day"] == day:
        with open(file_path, "r") as letter:
            random_letter = letter.read()
            new_letter = random_letter.replace("[NAME]", person["name"])
            try:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=MY_EMAIL, password=PASSWORD)
                    connection.sendmail(from_addr=MY_EMAIL, to_addrs=person["email"],
                                        msg=f"Subject:{TITLE_MAIL}\n\n"
                                            f"{new_letter}")
            except Exception as e:
                print("Error:", e)

