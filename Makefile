CONTAINERS=-f mongodb -f statsapi
MAIN_COMPOSE=./docker-compose.yml
IMAGES := mongodb statsapi
COMPOSES=-f $(MAIN_COMPOSE)

up:
	docker volume create mongo_db_data
	docker compose -f $(MAIN_COMPOSE) up -d --force-recreate --build --remove-orphans $(IMAGES) 
down:
	docker compose $(COMPOSES) down -v
	