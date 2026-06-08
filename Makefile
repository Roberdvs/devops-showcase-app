KIND_CLUSTER ?= e2e
LOCAL_IMAGE ?= devops-showcase-app:local

dev:
	docker compose up --watch --build

test:
	uv run coverage run -m pytest app/tests/unit/
	uv run coverage report

integration-tests:
	PYTHONPATH=. uv run pytest app/tests/integration/ -v

build:
	docker build -t $(LOCAL_IMAGE) .

helm-deps:
	cd helm/devops-showcase-app && helm dependency update

helm-install:
	cd helm/devops-showcase-app && helm install devops-showcase-app . --namespace devops-showcase-app --create-namespace $(HELM_ARGS)

helm-upgrade:
	cd helm/devops-showcase-app && helm upgrade devops-showcase-app . --namespace devops-showcase-app $(HELM_ARGS)

helm-uninstall:
	cd helm/devops-showcase-app && helm uninstall devops-showcase-app --namespace devops-showcase-app

e2e-test:
	./scripts/e2e-test.sh

kind-create:
	@kind get clusters | grep -q '^$(KIND_CLUSTER)$$' || kind create cluster --name $(KIND_CLUSTER)

kind-delete:
	kind delete cluster --name $(KIND_CLUSTER)

kind-load: build
	kind load docker-image $(LOCAL_IMAGE) --name $(KIND_CLUSTER)

# Mirror the CI e2e flow locally on a kind cluster: build and load the local
# image, install the chart with it, then run the e2e tests. The cluster is left
# running for inspection; tear it down with `make kind-delete`.
e2e-local: kind-create kind-load helm-deps
	cd helm/devops-showcase-app && helm upgrade --install devops-showcase-app . \
		--namespace devops-showcase-app --create-namespace \
		--set application.deployment.image.repository=devops-showcase-app \
		--set application.deployment.image.tag=local
	$(MAKE) e2e-test
