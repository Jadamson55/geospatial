# -------------------------------------
# MAKEFILE
# -------------------------------------

# Parse docker container name prefix from working dir
ifeq ($(OS),Windows_NT)
	NAME := $(notdir $(CURDIR))
	LOCATION := $(CURDIR)
else
	NAME := $(shell basename $$PWD | sed -e s/[_\\.]//g)
	LOCATION := $(shell pwd -P)
endif

PROJECT := ignored

CONTAINER_NAME ?= "geospatial"

.DEFAULT_GOAL := help


# Project Commands
# =====================================

.PHONY: buildnc
buildnc: ## Build all containers
	docker-compose -p ${NAME} --verbose build --no-cache

.PHONY: build
build: ## Build all containers
	docker-compose -p ${NAME} --verbose build

.PHONY: up
up: ## Bring up all containers
	docker-compose -p ${NAME} up -d

.PHONY: start
start: up

.PHONY: stop
stop:
	docker-compose -p ${NAME} stop

.PHONY: down
down:
	docker-compose -p ${NAME} down

.PHONY: shell
shell: ## Run a bash session on a container
	docker exec -it ${CONTAINER_NAME}_1 /bin/bash

