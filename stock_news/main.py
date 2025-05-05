import requests
import datetime as dt
from twilio.rest import Client
import os
import random
from dotenv import load_dotenv

#----------------CONSTANTS-----------------#
STOCK = "Bitcoin"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#---------------ENV VARIABLES---------------#
load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
api_stock = os.getenv("API_STOCK")
api_news = os.getenv("API_NEWS")
phone_number = os.getenv("PHONE_NUMBER")
virtual_phone = os.getenv("VIRTUAL_PHONE")

#------------DATETIME FUNCTIONS-----------#
yesterday = dt.datetime.now().date() - dt.timedelta(days=1)
today = dt.datetime.now().date()

#-------------API CALLS-------------#
parameters = {
    "q": "bitcoin",
    "from": yesterday,
    "to": today,
    "sortBy": "popularity",
    "apikey": api_news
}

stock_params = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": "BTC",
    "market": "USD",
    "apikey": api_stock
}

response_stock = requests.get(STOCK_ENDPOINT, params=stock_params)
response_stock.raise_for_status()
stock_data = response_stock.json()
price_data = stock_data["Time Series (Digital Currency Daily)"]
today_close = float(price_data[str(today)]["4. close"])
yesterday_close = float(price_data[str(yesterday)]["4. close"])


def main():
    percentage_change = ((today_close - yesterday_close) / yesterday_close) * 100
    if percentage_change > 5:
        response_news = requests.get(NEWS_ENDPOINT, params=parameters)
        response_news.raise_for_status()
        data = response_news.json()
        articles = data["articles"][0:3]
        random_article = random.choice(articles)
        symbol = "🔺" if today_close > yesterday_close else "🔻"
        message_body = (
            f"{STOCK}: {symbol}{percentage_change:.2f}%,\n\n"
            f"Headline: {random_article['title']}\n\n"
            f"Brief: {random_article['description']}")
        client = Client(account_sid, auth_token)
        try:
            message = client.messages.create(
                from_=virtual_phone,
                body=message_body,
                to=phone_number
            )
            print("Message SID:", message.sid)
        except Exception as e:
            print("Failed to send message:", e)


if __name__ == "__main__":
    main()
