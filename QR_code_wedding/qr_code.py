import qrcode
from dotenv import load_dotenv
import os

## creating qrcode

load_dotenv()

URL = os.getenv("URL")
data= URL
img = qrcode.make(data)

img.save("static/images/my_qrcode.png")

