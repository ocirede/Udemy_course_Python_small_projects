from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib


load_dotenv()
class NotificationManager:
    def __init__(self):
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.phone_number = os.getenv("PHONE_NUMBER")
        self.auth_token = os.getenv("AUTH_TOKEN")
        self.email = os.getenv("MY_EMAIL")
        self.password_email = os.getenv("PASSWORD_EMAIL")
        self.virtual_phone_number = os.getenv("VIRTUAL_PHONE")
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, flight_infos):
        try:
            message = self.client.messages.create(
                from_= self.virtual_phone_number,
                body=flight_infos,
                to= self.phone_number
            )
            if len(flight_infos) > 160:
                print("Warning: message exceeds 160 characters")
                print(len(flight_infos))
            print("Message SID:", message.sid)
            return message
        except Exception as e:
            print("Failed to send message:", e)
            return None


    def send_emails(self, flight_infos, email):
        title_mail = "Flight to Colombia"
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user= self.email , password=self.password_email)
                connection.sendmail(from_addr=self.email , to_addrs=email,
                                    msg=f"Subject:{title_mail}\n\n"
                                        f"{flight_infos}")
        except Exception as e:
            print("Error:", e)



