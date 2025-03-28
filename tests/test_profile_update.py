import pytest
from fixtures.helpers import login, update_profile, get_profile, generate_random_name, pretty_print
from fixtures.credentials import LOGIN, PASSWORD


@pytest.fixture(scope="session")
def auth_cookie():
    """Фикстура с мягкой обработкой ошибок"""
    try:
        cookie, req, resp = login(LOGIN, PASSWORD, return_full=True)
        status = resp.status_code == 200 if resp else False
        pretty_print(
            "Аутентификация",
            req,
            resp,
            "Успешная аутентификация!" if status else "",
            "Ошибка аутентификации!"
        )
        return cookie if status else None
    except Exception as e:
        pretty_print(
            "Аутентификация",
            None,
            None,
            "",
            f"Критическая ошибка: {str(e)}"
        )
        return None


def test_profile_update_flow(auth_cookie):
    """Тест с продолжением выполнения после ошибок"""
    # ШАГ 1: Всегда выполняем аутентификацию
    auth_success = auth_cookie is not None

    # ШАГ 2: Обновление профиля
    update_success = False
    test_data = {"name": "", "surname": ""}
    update_req, update_resp = None, None

    if auth_success:
        try:
            test_data = {
                "name": generate_random_name(),
                "surname": generate_random_name()
            }
            update_response = update_profile(test_data["name"], test_data["surname"], auth_cookie)
            update_success = update_response.status_code == 200
            update_req = update_response.request
            update_resp = update_response
        except Exception as e:
            update_req = getattr(e, 'request', None)
            update_resp = getattr(e, 'response', None)

    # Всегда выводим шаг обновления
    pretty_print(
        "Обновление профиля",
        update_req,
        update_resp,
        "Профиль обновлен!" if update_success else "",
        "Ошибка обновления!" if auth_success else "Пропущено (аутентификация)"
    )

    # ШАГ 3: Проверка данных
    profile_check = False
    profile_req, profile_resp = None, None

    if auth_success:
        try:
            profile_data, profile_req, profile_resp = get_profile(auth_cookie, return_full=True)
            profile_check = (
                    profile_data.get("name") == test_data["name"] and
                    profile_data.get("surname") == test_data["surname"]
            )
        except Exception as e:
            profile_req = getattr(e, 'request', None)
            profile_resp = getattr(e, 'response', None)

    pretty_print(
        "Проверка данных",
        profile_req,
        profile_resp,
        "Данные совпадают!" if profile_check else "",
        "Данные не совпадают!" if auth_success else "Пропущено (аутентификация)"
    )

    # Итоговые проверки
    assert auth_success, "Аутентификация не пройдена"
    assert update_success, "Обновление профиля не выполнено"
    assert profile_check, "Данные профиля не соответствуют"