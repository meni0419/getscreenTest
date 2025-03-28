# Используем официальный образ Python с Alpine (легковесный)
FROM python:3.12-alpine

# Устанавливаем системные зависимости
RUN apk add --no-cache gcc musl-dev libffi-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/

# Команда запуска тестов (можно переопределить при запуске)
CMD ["pytest", "src/tests/", "-v"]