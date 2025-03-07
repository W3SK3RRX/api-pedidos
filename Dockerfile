# Usar a imagem oficial do Python Alpine
FROM python:3.13.2-alpine3.21

# Instalar dependências do sistema e Bash
RUN apk add --no-cache bash gcc musl-dev libffi-dev postgresql-dev

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório de logs e arquivos estáticos (fora do volume)
RUN mkdir -p /app/logs /app/staticfiles && touch /app/logs/api_access.log

# Garantir que o comando 'chown' seja executado como root
#USER root
#UN chown -R www-data:www-data /app/logs /app/staticfiles

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação usando Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "config.wsgi:application"]
