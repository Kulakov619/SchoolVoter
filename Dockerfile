FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Копируем проект
COPY app/ /app/

# Среда и переменные окружения
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    DATA_DIR=/app/data

# Создаём директорию для данных голосования
RUN mkdir -p /app/data

# Открываем порт
EXPOSE 5000

# Запускаем через gunicorn (надёжный WSGI-сервер)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]