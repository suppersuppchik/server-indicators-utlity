CONTAINERS=-f mongodb -f statsapi 
MAIN_COMPOSE=./docker-compose.yml
IMAGES := mongodb statsapi 
COMPOSES=-f $(MAIN_COMPOSE)

up:
	docker volume create dbdata6
	docker compose -f $(MAIN_COMPOSE) up -d --force-recreate --build --remove-orphans $(IMAGES) 
uplistener:
	ls
	source ./aislr4_system_listenner_service/venv/bin/activate
	python ./aislr4_system_listenner_service/main.py
down:
	docker compose $(COMPOSES) down -v
	