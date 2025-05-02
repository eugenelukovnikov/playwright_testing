# Сборка docker build -t playwright-tests . --no-cache
# официальный Playwright
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy 

ENV PYTHONPATH=/app

# зависимости, системные пакеты
RUN apt-get update && \
    apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копируем проект
WORKDIR /app
COPY . .

# Устанавливаем Python-зависимости
RUN pip install -r requirements.txt

# Запускаемся docker run -it --rm playwright-tests
CMD ["pytest", "--alluredir=./allure-results"]