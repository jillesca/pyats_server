include .env.example

.PHONY: run

run:
	uvicorn main:app --host 0.0.0.0 --reload --port $(PYATS_SERVER_PORT)

container-run:
	-$(MAKE) stop-container
	docker compose up --build --detach pyats_server

stop-container:
	-docker compose down pyats_server
	-docker compose rm -f pyats_server

follow:
	docker compose logs --follow pyats_server