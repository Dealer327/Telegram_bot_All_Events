FROM python:3.11.5


# Устанавливаем рабочую директорию
WORKDIR /app
ENV PYTHONUNBUFFERED 1


COPY . .
# Копируем файл requirements.txt


# Копируем файл .env
COPY .env.docker /app/.env
COPY requirements.txt .
# Устанавливаем зависимости
RUN pip install -r requirements.txt



# Копируем остальные файлы проекта
# Запускаем сервер Django

