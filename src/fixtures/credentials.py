import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")
CAPTCHA_TYPE = os.getenv("CAPTCHA_TYPE")

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}