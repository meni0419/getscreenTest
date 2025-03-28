# fixtures/helpers.py
import random
import string
import requests
from typing import Optional
from fixtures.credentials import BASE_URL, HEADERS, CAPTCHA_TYPE
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import logging


def login(login: str, password: str) -> Optional[str]:
    """Аутентификация с динамическим токеном и полными заголовками"""
    url = f"{BASE_URL}/login"

    payload = {
        "login": login,
        "password": password,
        "captcha_type": CAPTCHA_TYPE
    }

    # Полный набор заголовков из примера запроса
    full_headers = {
        **HEADERS,
        "Origin": "https://getscreen.dev",
        "Referer": "https://getscreen.dev/login",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    try:
        with requests.Session() as session:
            # Первый запрос для получения CSRF-токена (если требуется)
            session.get("https://getscreen.dev/login")

            # Основной запрос аутентификации
            response = session.post(
                url,
                data=payload,
                headers=full_headers,
                allow_redirects=False
            )

            # Проверка успешной аутентификации
            if response.status_code == 200 and response.json().get("status") == 0:
                return session.cookies.get("llt", domain=".getscreen.dev")

            print(f"Auth failed. Response: {response.text}")
            return None

    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return None


# fixtures/helpers.py
def update_profile(name: str, surname: str, auth_cookie: str) -> requests.Response:
    """Обновление профиля с полными заголовками и сессией"""
    url = f"{BASE_URL}/dashboard/settings/account/update"

    # Используем сессию для сохранения cookies
    with requests.Session() as session:
        session.cookies.update({"llt": auth_cookie})

        headers = {
            "Content-Type": "application/json",
            "Referer": f"{BASE_URL}/dashboard/settings/account",
            "Origin": BASE_URL,
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }

        payload = {
            "name": name,
            "surname": surname,
            "ad_allowed": False,
            "beta": True,
            "country": "am",
            "dateformat": 0,
            "language": "en",
            "timezone": 0
        }

        # Добавляем все cookies из браузера (пример)
        session.cookies.update({
            "lang": "en",
            "cc_cookie": "..."
        })

        response = session.post(url, json=payload, headers=headers)
        return response


def get_profile(auth_cookie: str) -> dict:
    """Получение профиля с проверкой статуса"""
    url = f"{BASE_URL}/dashboard/settings/account"
    headers = {"Cookie": f"llt={auth_cookie}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def generate_random_name(length: int = 8) -> str:
    """Генерация случайного имени"""
    first_char = random.choice(string.ascii_uppercase)
    rest = ''.join(random.choices(string.ascii_lowercase, k=length - 1))
    return first_char + rest

from colorama import Fore, Style
import json


def pretty_print(step_name, request, response, success_message, error_message):
    separator = "=" * 30
    print(f"{Fore.BLUE}{separator} Шаг: {step_name} {separator}{Style.RESET_ALL}\n")

    # Request details
    print(f"{Fore.YELLOW}{separator} Request Details {separator}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}URL: {Style.RESET_ALL}{request.url}")
    print(f"{Fore.CYAN}Method: {Style.RESET_ALL}{request.method}")
    print(f"{Fore.CYAN}Headers: {Style.RESET_ALL}{request.headers}")
    if request.body:
        try:
            body = json.loads(request.body) if isinstance(request.body, str) else request.body
            pretty_body = json.dumps(body, indent=2, ensure_ascii=False)
            print(f"{Fore.CYAN}Body: {Style.RESET_ALL}{pretty_body}")
        except json.JSONDecodeError:
            print(f"{Fore.CYAN}Body: {Style.RESET_ALL}{request.body}")

    print()

    # Response details
    print(f"{Fore.YELLOW}{separator} Response Details {separator}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Status Code: {Style.RESET_ALL}{response.status_code}")
    try:
        response_content = response.json()
        pretty_response = json.dumps(response_content, indent=2, ensure_ascii=False)
    except (ValueError, json.JSONDecodeError):
        pretty_response = response.text
    print(f"{Fore.MAGENTA}Response: {Style.RESET_ALL}{pretty_response}\n")

    # Status message
    if response.status_code == 200:
        print(f"{Fore.GREEN}[Succeed]{Style.RESET_ALL} {success_message}\n")
    else:
        print(f"{Fore.RED}[Failed]{Style.RESET_ALL} {error_message}\n")
