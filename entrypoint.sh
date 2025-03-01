#!/bin/sh

echo "Aguardando banco de dados..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Banco de dados disponível!"

# Aplicar migrações
echo "Rodando migrações..."
python manage.py migrate

# Iniciar servidor Gunicorn
echo "Iniciando servidor..."
exec gunicorn -b 0.0.0.0:8000 config.wsgi:application
