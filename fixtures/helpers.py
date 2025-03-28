import random
import string
from fixtures.credentials import BASE_URL, HEADERS, CAPTCHA_TYPE
from requests.exceptions import RequestException
import logging
import requests


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


# helpers.py (измененная функция pretty_print)
def pretty_print(step_name, request, response, success_message, error_message):
    """Полная версия с детализацией"""
    separator = "=" * 30
    print(f"\n{Fore.BLUE}{separator} Шаг: {step_name} {separator}{Style.RESET_ALL}\n")

    # Детали запроса
    print(f"{Fore.YELLOW}{separator} Детали запроса {separator}{Style.RESET_ALL}")
    if request:
        print(f"{Fore.CYAN}URL:{Style.RESET_ALL} {request.url}")
        print(f"{Fore.CYAN}Method:{Style.RESET_ALL} {request.method}")
        print(f"{Fore.CYAN}Headers:{Style.RESET_ALL} {dict(request.headers)}")
        if request.body:
            try:
                body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
                print(f"{Fore.CYAN}Body:{Style.RESET_ALL}\n{json.dumps(json.loads(body), indent=2)}")
            except:
                print(f"{Fore.CYAN}Body:{Style.RESET_ALL} {body}")
    else:
        print(f"{Fore.RED}Запрос отсутствует{Style.RESET_ALL}")

    # Детали ответа
    print(f"\n{Fore.YELLOW}{separator} Детали ответа {separator}{Style.RESET_ALL}")
    if response:
        print(f"{Fore.CYAN}Status:{Style.RESET_ALL} {response.status_code}")
        try:
            print(f"{Fore.CYAN}Response:{Style.RESET_ALL}\n{json.dumps(response.json(), indent=2)}")
        except:
            print(f"{Fore.CYAN}Response:{Style.RESET_ALL} {response.text}")
    else:
        print(f"{Fore.RED}Ответ отсутствует{Style.RESET_ALL}")

    # Статус
    status_icon = f"{Fore.GREEN}[Success]" if success_message else f"{Fore.RED}[Failed]"
    print(f"\n{status_icon} {success_message or error_message}{Style.RESET_ALL}\n")