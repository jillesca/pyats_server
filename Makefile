include .env.example

.PHONY: run

DOCKER := $(shell command -v docker 2> /dev/null || echo podman)

run:
	uvicorn main:app --host 0.0.0.0 --reload --port $(PYATS_SERVER_PORT)

container-run:
	-$(MAKE) stop-container
	$(DOCKER) compose up --build --detach pyats_server

stop-container:
	-$(DOCKER) compose down pyats_server
	-$(DOCKER) compose rm -f pyats_server

follow:
	$(DOCKER) compose logs --follow pyats_server