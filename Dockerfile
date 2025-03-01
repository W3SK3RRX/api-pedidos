# Usar a imagem oficial do Python Alpine
FROM python:3.13.2-alpine3.21

# Instalar dependências do sistema
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Criar diretório de logs (evita erro se não existir)
RUN mkdir -p logs && touch logs/api_access.log

# Expor a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação usando Gunicorn e WhiteNoise
CMD ["gunicorn", "-b", "0.0.0.0:8000", "config.wsgi:application"]
