dev:
	docker compose up --watch --build

test:
	uv run coverage run -m pytest
	uv run coverage report

build:
	docker build -t sample-app:local .

helm-deps:
	cd helm/sample-app && helm dependency update

helm-install:
	cd helm/sample-app && helm install sample-app . --namespace sample-app --create-namespace

helm-upgrade:
	cd helm/sample-app && helm upgrade sample-app . --namespace sample-app

helm-uninstall:
	cd helm/sample-app && helm uninstall sample-app --namespace sample-app
