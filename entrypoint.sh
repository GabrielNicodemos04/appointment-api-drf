#!/bin/bash
set -e

echo "Aplicando migrações..."
python core/manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python core/manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --worker-timeout 60 \
    --access-logfile - \
    --error-logfile -
