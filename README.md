# Full Stack FastAPI Base Project Template

This is a project template which uses:
- [FastAPI](https://fastapi.tiangolo.com/) as backend part.
- [Vue.js](https://vuejs.org/) as frontend part(Vuetify + TypeScript).
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations.
- [SQLModel](https://sqlmodel.tiangolo.com/) as async ORM.

## Features

* Full **Docker** integration(Docker based).
* **Docker Compose** integration for local development.
* Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend.
* **Secure password** hashing by default.
* **JWT token** authentication.
* Basic starting models for users and roles (modify and remove as you need).
* **Alembic** migrations.
* **CORS** (Cross Origin Resource Sharing).
* **Vue** frontend.
* **PGAdmin** for PostgreSQL database.

## How to use it

### Set environment variables

For backend create an **.env** file on **backend** folder and copy the content from 
**.env.example**. 
Change it according to your own configuration.

```
PROJECT_NAME - name for your application.
SERVER_HOST - hostname for your application.
API_VERSION - version of your API.
API_PREFIX - URL prefix for your API.

SECRET_KEY - sectet key.

FIRST_SUPERUSER_EMAIL - first superuser email.
FIRST_SUPERUSER_PASSWORD - first superuser password.

DB_SCHEME - database scheme.
DB_USER - database username.
DB_PASSWORD - database password.
DB_HOST - database hostname.
DB_PORT - database port.
DB_NAME - database name.

SMTP_TLS - using tls for smtp mailing(True or False).
SMTP_PORT - smtp port.
SMTP_HOST - smtp hostname.
SMTP_USER - smtp username.
SMTP_PASSWORD - smtp password.

EMAILS_ENABLED - enable mailing(True or False).
EMAILS_FROM_EMAIL - email from which emails will be sent.
EMAILS_FROM_NAME - email sender name.
EMAILS_TEMPLATES_DIR - emails html templates directory.
EMAILS_RESET_TOKEN_EXPIRE_HOURS - amount of hours when reset token will be expired.

ASYNC_DB_URI - async database url as "postgresql://username:password@host:5432/database"

JWT_ALGORITHM - jwt algorithm of encoding.

BACKEND_CORS_ORIGINS - list of allowed cors origins.
```

For frontend create an **.env** file on **frontend** folder and copy the content from 
**.env.example**. 

```
VUE_APP_DOMAIN_DEV - domain name for development.
VUE_APP_DOMAIN_STAG - domain name for staging.
VUE_APP_DOMAIN_PROD - domain name for production.
VUE_APP_NAME - application name
VUE_APP_ENV - application environment(development, staging, production)
```

### Run the project using Docker containers and forcing build containers

*Using docker compose command*
```bash
docker-compose up --build
```

*Using Makefile command*
```bash
make run-build
```

### Run project using Docker containers

*Using docker compose command*
```bash
docker-compose up
```

*Using Makefile command*
```bash
make run
```

### Setup database with initial data

This creates sample users and roles on database.

*Using docker compose command*
```bash
docker-compose exec server python app/initial_data.py
```

*Using Makefile command*
```bash
make init-db
```

Any of the above commands creates three users with the following passwords:

- **Admin credentials** 
  - *username:* admin@admin.com
  - *password:* admin 
- **Manager credentials**
  - *username:* manager@example.com
  - *password:* admin 
- **User credentials** 
  - *username:* user@example.com
  - *password:* admin 

You can connect to the Database using pgAdmin4 and use the credentials from .env file. 
Database port on local machine has been configured to **5432** on docker-compose.yml file