#!/usr/bin/make

include ./backend/.env

define SERVERS_JSON
{
	"Servers": {
		"1": {
			"Name": "fastapi-alembic",
			"Group": "Servers",
			"Host": "$(DB_HOST)",
			"Port": 5432,
			"MaintenanceDB": "postgres",
			"Username": "$(DB_PASSWORD)",
			"SSLMode": "prefer",
			"PassFile": "/tmp/pgpassfile"
		}
	}
}
endef
export SERVERS_JSON

help:
	@echo "make"
	@echo "    run-build"
	@echo "        Run docker compose and force build containers."
	@echo "    run"
	@echo "        Run docker compose."
	@echo "    stop"
	@echo "        Stop docker compose."
	@echo "    init-db"
	@echo "        Init database with sample data."
	@echo "    add-migration"
	@echo "        Add new database migration using alembic."

run-build:
	docker-compose -f docker-compose.yml up --build

run:
	docker-compose -f docker-compose.yml up

stop:
	docker-compose -f docker-compose.yml down

init-db:
	docker-compose -f docker-compose.yml exec server python app/initial_data.py

add-migration:
	docker-compose -f docker-compose.yml exec server alembic revision --autogenerate && \
	docker-compose -f docker-compose.yml exec server alembic upgrade head
