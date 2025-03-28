import pytest
from time import sleep
from fixtures.helpers import login, update_profile, get_profile, generate_random_name, pretty_print
from fixtures.credentials import LOGIN, PASSWORD


@pytest.fixture(scope="session")
def auth_cookie():
    """Фикстура с обработкой ошибок подключения"""
    try:
        cookie, req, resp = login(LOGIN, PASSWORD, return_full=True)
        pretty_print(
            "Аутентификация",
            req,
            resp,
            "Успешная аутентификация!",
            "Ошибка аутентификации!"
        )
        if not cookie:
            pytest.fail("Authentication failed: No cookie received")
        return cookie
    except Exception as e:
        pytest.fail(f"Authentication setup failed: {str(e)}")


def test_profile_update_flow(auth_cookie):
    """Тест обновления профиля"""
    test_data = {
        "name": generate_random_name(),
        "surname": generate_random_name()
    }

    # ШАГ 1: Обновление профиля
    update_response = update_profile(test_data["name"], test_data["surname"], auth_cookie)
    assert update_response.status_code == 200, f"Update failed: {update_response.text}"
    pretty_print(
        "Обновление профиля",
        update_response.request,
        update_response,
        "Профиль обновлен!",
        "Ошибка обновления!"
    )

    sleep(0.5)

    # ШАГ 2: Проверка изменений
    profile_data, profile_req, profile_resp = get_profile(auth_cookie, return_full=True)
    pretty_print(
        "Проверка данных профиля",
        profile_req,
        profile_resp,
        "Данные профиля получены!",
        "Ошибка получения данных!"
    )

    assert profile_data["name"] == test_data["name"], "Имя не совпадает"
    assert profile_data["surname"] == test_data["surname"], "Фамилия не совпадает"