FROM python:3.10-slim

# Создание рабочей директории
WORKDIR /tablebot

# Копирование списка зависимостей Python
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

CMD ["python", "run.py"]