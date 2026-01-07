import qrcode
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")
data= URL
img = qrcode.make(data)

img.save("my_qrcode.png")

