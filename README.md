## Ссылка на тестовое задание
https://docs.google.com/document/d/13tKyuUiSZFhKADUdO_XzZE8MqYDGiQhCpJa9G3wmQHQ

# Инструкция по запуску автотеста

# Запуск автотестов

## Вариант 1: С использованием Docker 🐳

### Предварительные требования

- Установленный [Docker](https://docs.docker.com/get-docker/)
- Установленный [Docker Compose](https://docs.docker.com/compose/install/)

### Шаги:

1. **Создайте `.env` файл** (если его нет):
   ```bash
   cp .env.example .env
   ```
   Заполните `.env` файл актуальными данными:
   ```ini
   LOGIN=your_login
   PASSWORD=your_password
   BASE_URL=https://getscreen.dev/api
   CAPTCHA_TYPE=google
   ```
2. **Соберите Docker-образ:**
   ```bash
   docker-compose build
   ```
3. **Запустите тесты:**
   ```bash
   docker-compose up
   ```
4. *(Опционально)* Запуск с дополнительными параметрами:
   ```bash
   docker-compose run api-tests pytest src/tests/ -s -v
   ```

## Вариант 2: Без использования Docker 💻

### Предварительные требования

- Python версии 3.8+
- Установленный `pip`

### Шаги:

1. **Создайте виртуальное окружение (рекомендуется):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate.bat  # Для Windows
   ```
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Создайте/настройте `.env` файл** (см. шаг 1 Docker-варианта).

4. **Запустите тесты:**
   ```bash
   pytest src/tests/ -v
   ```

## Дополнительные опции 🛠

### Генерация отчета Allure

- **С использованием Docker:**
  ```bash
  docker-compose run api-tests pytest src/tests/ --alluredir=./reports
  ```
- **Без использования Docker:**
  ```bash
  pytest src/tests/ --alluredir=./reports
  ```

### Запуск конкретного теста

```bash
pytest src/tests/test_profile_update.py::test_profile_update_flow -v
```

### Очистка Docker-окружения

```bash
docker-compose down --rmi all --volumes
```
