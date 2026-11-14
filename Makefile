.PHONY: build run stop

build:
	docker compose build

run:
	docker compose up -d --build --wait --wait-timeout 60

stop:
	docker compose down
