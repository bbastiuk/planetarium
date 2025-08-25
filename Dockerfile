# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip \
  && pip install 'drf-spectacular[sidecar]' \
  && pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/media/uploads && chmod -R 755 /app/media

CMD ["gunicorn", "planetarium_api.wsgi:application", "--bind", "0.0.0.0:8000"]