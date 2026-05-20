#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-devops-showcase-app}"
RELEASE_NAME="${RELEASE_NAME:-devops-showcase-app}"
TIMEOUT="${TIMEOUT:-300s}"

echo "=== Waiting for pods to be ready ==="
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name="$RELEASE_NAME" \
  -n "$NAMESPACE" \
  --timeout="$TIMEOUT"
echo "Application is ready"

echo ""
echo "=== Resolving service URL ==="
SERVICE_URL=$(minikube service "$RELEASE_NAME" --url -n "$NAMESPACE")
echo "Testing application at: $SERVICE_URL"

echo ""
echo "=== Testing health endpoints ==="
curl -f "$SERVICE_URL/health/live"
curl -f "$SERVICE_URL/health/ready"

echo ""
echo "=== Testing API docs ==="
curl -f "$SERVICE_URL/docs" > /dev/null

echo ""
echo "=== Testing metrics endpoint ==="
curl -f "$SERVICE_URL/metrics" > /dev/null

echo ""
echo "=== Testing hello endpoint (create user) ==="
curl -f -X PUT "$SERVICE_URL/hello/testuser" \
  -H "Content-Type: application/json" \
  -d '{"dateOfBirth": "1990-01-15"}'

echo ""
echo "=== Testing hello endpoint (get user) ==="
curl -f "$SERVICE_URL/hello/testuser"

echo ""
echo "All tests passed! 🎉"
