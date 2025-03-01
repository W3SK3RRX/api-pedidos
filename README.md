# API de Pedidos

Este é um projeto de API para gerenciamento de pedidos em restaurantes, desenvolvido utilizando Django REST Framework e Docker para orquestração dos containers. A API permite que restaurantes gerenciem seus pedidos, clientes acompanhem o status em tempo real e administradores supervisionem o sistema.

## ✨ Tecnologias Utilizadas

- **Backend**: Django (Django REST Framework)
- **Banco de Dados**: PostgreSQL
- **WebSockets**: Django Channels para atualizações em tempo real
- **Autenticação**: JWT + 2FA (Autenticação de Dois Fatores)
- **Orquestração de Containers**: Docker & Docker Compose
- **Servidor de Aplicação**: Gunicorn

## 🔧 Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em seu ambiente de desenvolvimento:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.12 ou superior](https://www.python.org/downloads/)
- [Pipenv ou Poetry](https://pipenv.pypa.io/en/latest/) (caso esteja usando um ambiente virtual)

## 💻 Como Executar o Projeto

Siga os passos abaixo para rodar o projeto em seu ambiente local:

### 1. **Clonar o Repositório**

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/W3SK3RRX/api-pedidos.git
cd api-pedidos
```

### 2. **Configuração do Docker**

O projeto utiliza o Docker e o Docker Compose para facilitar a execução dos containers. Para rodar o projeto no Docker, basta usar o comando:

```bash
docker-compose up -d --build
```

Esse comando irá:

- Criar os containers para o banco de dados (PostgreSQL) e o backend (Django).
- Rodar o servidor Django no container **django_api_pedidos** e o banco de dados no container **db_api_pedidos**.

### 3. **Acessar o Container do Django**

Depois que os containers estiverem em execução, entre no container do Django para rodar as migrações:

```bash
docker exec -it django_api_pedidos bash
```

### 4. **Executar as Migrações do Banco de Dados**

Dentro do container, execute as migrações para configurar o banco de dados:

```bash
python manage.py migrate
```

### 5. **Criar um Superusuário (opcional)**

Para acessar o painel administrativo do Django, você pode criar um superusuário com o comando:

```bash
python manage.py createsuperuser
```

### 6. **Rodar o Servidor**

O servidor do Django já estará sendo executado dentro do container na porta 8000. Você pode acessá-lo no navegador usando o seguinte endereço:

```bash
http://localhost:8000
```

Caso precise rodar o servidor manualmente, execute o comando:

```bash
python manage.py runserver 0.0.0.0:8000
```

### 7. **Verificar Logs do Docker (opcional)**

Se você deseja acompanhar os logs do seu container para verificar a execução, use o comando:

```bash
docker logs -f django_api_pedidos
```

### 8. **Variáveis de Ambiente**

As variáveis de ambiente são configuradas através do arquivo `.env`. Certifique-se de que as seguintes variáveis estejam configuradas corretamente:

```ini
# Configurações do Django
SECRET_KEY=supersecretkey123
DEBUG=True
ALLOWED_HOSTS=*

# Banco de Dados
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Configurações de E-mail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seuemail@gmail.com
EMAIL_HOST_PASSWORD=suasenha
EMAIL_USE_TLS=True
```

### 9. **Comandos Úteis**

Verificar o status do banco de dados (PostgreSQL):
```bash
docker-compose logs db_api_pedidos
```

Parar e remover os containers:
```bash
docker-compose down
```

Reiniciar o projeto (containers e volumes):
```bash
docker-compose down -v
docker-compose up -d
```

### 10. **Contribuindo**

Contribuições são sempre bem-vindas! Para contribuir com o projeto:

1. Faça um fork do repositório.
2. Crie uma nova branch
   ```bash
   git checkout -b feature/nova-feature
   ```
4. Faça as alterações necessárias.
5. Faça o commit das suas alterações
   ```bash
   git commit -am 'Adiciona nova feature'
   ```
7. Envie para o seu repositório
   ```bash
   git push origin feature/nova-feature
   ```
8. Abra um Pull Request para o repositório original.

### 11. **Licença**

Este projeto está licenciado sob a Licença MIT.

