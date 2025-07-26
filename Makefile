dev:
	docker compose up --watch --build

test:
	uv run coverage run -m pytest app/tests/unit/
	uv run coverage report

integration-tests:
	PYTHONPATH=. uv run pytest app/tests/integration/ -v

build:
	docker build -t sample-app:local .

helm-deps:
	cd helm/sample-app && helm dependency update

helm-install:
	cd helm/sample-app && helm install sample-app . --namespace sample-app --create-namespace $(if $(IMAGE_TAG),--set application.deployment.image.tag=$(IMAGE_TAG))

helm-upgrade:
	cd helm/sample-app && helm upgrade sample-app . --namespace sample-app $(if $(IMAGE_TAG),--set application.deployment.image.tag=$(IMAGE_TAG))

helm-uninstall:
	cd helm/sample-app && helm uninstall sample-app --namespace sample-app
