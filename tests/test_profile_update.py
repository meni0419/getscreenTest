# tests/test_profile_update.py
import pytest
from time import sleep
from fixtures.helpers import login, update_profile, get_profile, generate_random_name
from fixtures.credentials import LOGIN, PASSWORD
from colorama import Fore, Style  # <-- добавь это


@pytest.fixture(scope="session")
def auth_cookie():
    """Фикстура для получения аутентификационной cookie"""
    cookie = login(LOGIN, PASSWORD)
    result = f"{Fore.GREEN}[Succeed]{Style.RESET_ALL}" if cookie else f"{Fore.RED}[Failed]{Style.RESET_ALL}"
    print(f"\nАутентификация по логину и паролю: {result}")
    if not cookie:
        pytest.fail("Authentication failed")
    return cookie


def test_profile_update_flow(auth_cookie):
    """Тест обновления профиля"""
    test_data = {
        "name": generate_random_name(),
        "surname": generate_random_name()
    }

    # ШАГ 1: Обновление профиля
    update_response = update_profile(test_data["name"], test_data["surname"], auth_cookie)

    print("\nИзменение полей имя и фамилия – HTTP-запрос:")
    print(f"URL: {update_response.request.url}")
    print(f"Метод: {update_response.request.method}")
    print(f"Заголовки запроса: {update_response.request.headers}")
    print(f"Тело запроса: {update_response.request.body}")

    print("\nОтвет сервера:")
    print(f"Статус: {update_response.status_code}")
    print(f"Тело ответа: {update_response.text}")

    result_update = f"{Fore.GREEN}[Succeed]{Style.RESET_ALL}" \
        if update_response.status_code == 200 else f"{Fore.RED}[Failed]{Style.RESET_ALL}"
    print(f"\nИзменение полей 'Имя' и 'Фамилия': {result_update}")

    assert update_response.status_code == 200, f"Update failed: {update_response.text}"

    sleep(0.5)

    # ШАГ 2: Проверка изменений
    profile_data = get_profile(auth_cookie)

    print("\nПолучение данных профиля – HTTP-запрос:")
    print(f"Полученные данные профиля: {profile_data}")

    check_passed = profile_data["name"] == test_data["name"] and profile_data["surname"] == test_data["surname"]
    result_check = f"{Fore.GREEN}[Succeed]{Style.RESET_ALL}" if check_passed else f"{Fore.RED}[Failed]{Style.RESET_ALL}"
    print("\nПолучение данных пользователя и проверка, что они изменились:", result_check)

    assert profile_data["name"] == test_data["name"], "Имя не совпадает"
    assert profile_data["surname"] == test_data["surname"], "Фамилия не совпадает"
