FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput || true

# Открываем порт
EXPOSE 8000

# Команда для запуска
CMD ["gunicorn", "team_finder.wsgi:application", "--bind", "0.0.0.0:8000"]