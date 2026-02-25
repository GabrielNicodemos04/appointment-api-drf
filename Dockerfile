FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install gunicorn \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python core/manage.py migrate --noinput; gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --worker-class sync --timeout 60 --access-logfile - --error-logfile -"]