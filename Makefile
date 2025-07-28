dev:
	docker compose up --watch --build

test:
	uv run coverage run -m pytest app/tests/unit/
	uv run coverage report

integration-tests:
	PYTHONPATH=. uv run pytest app/tests/integration/ -v

build:
	docker build -t devops-showcase-app:local .

helm-deps:
	cd helm/devops-showcase-app && helm dependency update

helm-install:
	cd helm/devops-showcase-app && helm install devops-showcase-app . --namespace devops-showcase-app --create-namespace $(HELM_ARGS)

helm-upgrade:
	cd helm/devops-showcase-app && helm upgrade devops-showcase-app . --namespace devops-showcase-app $(HELM_ARGS)

helm-uninstall:
	cd helm/devops-showcase-app && helm uninstall devops-showcase-app --namespace devops-showcase-app
