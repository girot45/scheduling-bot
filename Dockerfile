FROM python:3.10-slim

# Создание рабочей директории
WORKDIR /scheduling-bot

# Копирование списка зависимостей Python
COPY requirements.txt .

# COPY venv .

# RUN source /home/scheduling-bot/venv/bin/activate
# CMD ["source", "/home/scheduling-bot/venv/bin/activate"]

# Установка зависимостей Python
RUN pip install -r requirements.txt


# Копирование остальных файлов проекта
COPY . .

CMD ["python3", "run.py"]