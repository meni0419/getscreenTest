# fixtures/helpers.py
import random
import string
from fixtures.credentials import BASE_URL, HEADERS, CAPTCHA_TYPE
from requests.exceptions import RequestException
import logging
import json
import requests
from colorama import Fore, Style


def login(login: str, password: str, return_full: bool = False):
    """Аутентификация с обработкой ошибок подключения"""
    url = f"{BASE_URL}/login"
    payload = {
        "login": login,
        "password": password,
        "captcha_type": CAPTCHA_TYPE
    }

    full_headers = {
        **HEADERS,
        "Origin": "https://getscreen.dev",
        "Referer": "https://getscreen.dev/login",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        session = requests.Session()
        # Добавляем таймаут для первого запроса
        session.get("https://getscreen.dev/login", timeout=10)

        # Основной запрос с таймаутом
        response = session.post(
            url,
            data=payload,
            headers=full_headers,
            allow_redirects=False,
            timeout=10
        )

        # Всегда возвращаем валидные объекты запроса/ответа
        cookie = session.cookies.get("llt", domain=".getscreen.dev") if response.ok else None
        return (cookie, response.request, response) if return_full else cookie

    except Exception as e:
        logging.error(f"Critical login error: {str(e)}")
        # Создаем заглушки для объектов запроса/ответа
        dummy_request = requests.Request('POST', url)
        return (None, dummy_request, None) if return_full else None


def get_profile(auth_cookie: str, return_full: bool = False):
    """Получение профиля с возможностью возврата полных данных"""
    url = f"{BASE_URL}/dashboard/settings/account"
    headers = {"Cookie": f"llt={auth_cookie}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except (RequestException, ValueError) as e:
        data = {}
        response = getattr(e, "response", None)

    if return_full:
        return data, response.request, response
    return data


def update_profile(name: str, surname: str, auth_cookie: str) -> requests.Response:
    """Обновление профиля с полными заголовками и сессией"""
    url = f"{BASE_URL}/dashboard/settings/account/update"

    with requests.Session() as session:
        session.cookies.update({"llt": auth_cookie})

        headers = {
            **HEADERS,  # Используем базовые заголовки
            "Referer": f"{BASE_URL}/dashboard/settings/account",
            "Origin": BASE_URL,
            "X-Requested-With": "XMLHttpRequest"
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

        # Явно сериализуем в JSON и устанавливаем правильный Content-Type
        response = session.post(
            url,
            json=payload,
            headers=headers
        )
        return response


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

    # Request details с проверкой на None
    print(f"{Fore.YELLOW}{separator} Request Details {separator}{Style.RESET_ALL}")
    if request:
        print(f"{Fore.CYAN}URL: {Style.RESET_ALL}{getattr(request, 'url', 'N/A')}")
        print(f"{Fore.CYAN}Method: {Style.RESET_ALL}{getattr(request, 'method', 'N/A')}")
        print(f"{Fore.CYAN}Headers: {Style.RESET_ALL}{dict(getattr(request, 'headers', {}))}")
    else:
        print(f"{Fore.RED}Request object is missing{Style.RESET_ALL}")

    # Response details с проверкой на None
    print(f"\n{Fore.YELLOW}{separator} Response Details {separator}{Style.RESET_ALL}")
    if response:
        print(f"{Fore.MAGENTA}Status Code: {Style.RESET_ALL}{getattr(response, 'status_code', 'N/A')}")
        try:
            response_content = response.json()
            pretty_response = json.dumps(response_content, indent=2, ensure_ascii=False)
        except:
            pretty_response = getattr(response, 'text', 'Empty response')
        print(f"{Fore.MAGENTA}Response: {Style.RESET_ALL}{pretty_response}")
    else:
        print(f"{Fore.RED}Response object is missing{Style.RESET_ALL}")

    # Status message
    if response and response.status_code == 200:
        print(f"\n{Fore.GREEN}[Succeed]{Style.RESET_ALL} {success_message}")
    else:
        print(f"\n{Fore.RED}[Failed]{Style.RESET_ALL} {error_message}")
