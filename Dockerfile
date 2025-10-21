FROM python:3.11-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

RUN useradd -m voter && chown -R voter /app
USER voter

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]