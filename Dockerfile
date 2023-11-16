# Используйте базовый образ Python
FROM python:3.9

# Установка переменной окружения для не вывода буферизации вывода
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории в контейнере
WORKDIR /code

# Копирование зависимостей проекта и установка их через pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Копирование содержимого текущей директории в контейнер
COPY . /code/