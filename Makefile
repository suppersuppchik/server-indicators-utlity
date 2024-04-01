CONTAINERS=-f mongodb -f statsapi -f systemlistener
MAIN_COMPOSE=./docker-compose.yml
IMAGES := mongodb statsapi systemlistener
COMPOSES=-f $(MAIN_COMPOSE)

up:
	docker compose -f $(MAIN_COMPOSE) up -d --force-recreate --build --remove-orphans $(IMAGES) 
down:
	docker compose $(COMPOSES) down -v
	