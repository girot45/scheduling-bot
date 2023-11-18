FROM python:3.11-slim

# Создание рабочей директории
WORKDIR /scheduling-bot

# Копирование списка зависимостей Python
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Команда для запуска приложения
CMD ["python3", "run.py"]
