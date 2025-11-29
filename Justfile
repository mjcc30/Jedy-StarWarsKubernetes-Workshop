# Justfile for Jedy-StarWarsKubernetes

set shell := ["bash", "-c"]

# List all available commands
default:
    @just --list

# --- Local Development (Docker Compose) ---

# Run the app in development mode (Hot Reload)
dev:
    docker compose -f workshop/level-2-compose/compose.yaml up --build

# Run the app in production preview mode
preview:
    docker compose -f workshop/level-2-compose/compose.yaml -f workshop/level-2-compose/compose.production.yaml up --build

# Stop all docker compose containers
down:
    docker compose -f workshop/level-2-compose/compose.yaml down --remove-orphans

# --- Build Images (Level 1) ---

# Build the Backend Image
build-back:
    docker build -f workshop/level-1-docker/Dockerfile.back -t jedy-backend workshop/app/back

# Build the Frontend Image
build-front:
    docker build -f workshop/level-1-docker/Dockerfile.front -t jedy-frontend workshop/app/front

# --- Kubernetes Deployment ---

# Create the namespace starwars in Kubernetes
ns:
    kubectl create ns starwars --dry-run=client -o yaml | kubectl apply -f -

# Deploy the entire stack (Gateway, Configs, Apps, DB) to Kubernetes
deploy: ns
    @echo "🚀 Deploying Infrastructure (Gateway)..."
    kubectl apply -f workshop/level-5-sre/deploy/gatewayclass.yaml
    kubectl apply -f workshop/level-5-sre/deploy/gateway-infra.yaml
    @echo "📜 Deploying Configurations..."
    kubectl apply -f workshop/level-5-sre/deploy/back-configmap.yaml
    kubectl apply -f workshop/level-5-sre/deploy/front-configmap.yaml
    @echo "💾 Deploying Database (StatefulSet)..."
    kubectl apply -f workshop/level-5-sre/deploy/postgres.yaml
    @echo "🛸 Deploying Apps (Backend & Frontend)..."
    kubectl apply -f workshop/level-5-sre/deploy/back.yaml
    kubectl apply -f workshop/level-5-sre/deploy/front.yaml
    @echo "🛣️  Deploying Routes..."
    kubectl apply -f workshop/level-5-sre/deploy/routes.yaml
    kubectl apply -f workshop/level-6-mastery/deploy/dashboard-route.yaml
    @echo "✅ Done! Access via http://localhost"

# Delete all Kubernetes resources
undeploy:
    kubectl delete -f workshop/level-5-sre/deploy/ --ignore-not-found=true

# Force restart of pods (to pull new images or config)
restart:
    kubectl -n starwars rollout restart deployment back-deployment
    kubectl -n starwars rollout restart deployment front-deployment
    kubectl -n starwars rollout restart statefulset postgres-statefulset

# Force restart back-deployment (to pull new images or config)
restart-back:
    kubectl -n starwars rollout restart deployment back-deployment

# Force restart front-deployment (to pull new images or config)
restart-front:
    kubectl -n starwars rollout restart deployment front-deployment

# Force restart postgres-statefulset (to pull new images or config)
restart-postgres:
    kubectl -n starwars rollout restart statefulset postgres-statefulset

# --- Kubernetes Dashboard ---

# Install Kubernetes Dashboard via Helm
dashboard-install:
    helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
    helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard \
        --create-namespace --namespace kubernetes-dashboard \
        --set kong.proxy.http.enabled=true \
        --set kong.proxy.http.servicePort=80 \
        --set kong.proxy.http.containerPort=8000
    # Assuming dashboard-admin.yaml is in Level 6 or 5. Checking Level 5 first, then 6.
    kubectl apply -f workshop/level-6-mastery/deploy/dashboard-admin.yaml

# Generate Admin Token for Dashboard Login
dashboard-token:
    @echo "🔑 Copy this token to log in:"
    @kubectl -n kubernetes-dashboard create token admin-user

# Start Port-Forward (Fallback access)
dashboard-proxy:
    kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

# --- Observability & Scaling ---

# Install Metrics Server (Required for HPA)
install-metrics:
    kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
    kubectl patch -n kube-system deployment metrics-server --type=json \
      -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

# Deploy Horizontal Pod Autoscaler
deploy-hpa:
    kubectl apply -f workshop/level-5-sre/deploy/hpa.yaml

# Watch HPA status
watch-hpa:
    kubectl get hpa -n starwars --watch

# Start a K6 Load Test (Professional)
load-test:
    @echo "🧹 Cleaning previous tests..."
    -kubectl delete job k6-load-test -n starwars --ignore-not-found=true
    -kubectl delete configmap k6-script -n starwars --ignore-not-found=true
    @echo "📦 Creating ConfigMap..."
    kubectl create configmap k6-script -n starwars --from-file=workshop/level-5-sre/deploy/k6/script.js
    @echo "🚀 Starting K6 Job..."
    kubectl apply -f workshop/level-5-sre/deploy/k6/job.yaml
    @echo "👀 Following logs (Ctrl+C to stop following, test continues)..."
    @sleep 2
    kubectl logs -n starwars -f job/k6-load-test
    @echo "✅ Test finished! Check HPA status."

# 💥 Nuke Everything (Clean Slate)
reset-all:
    @echo "⚠️  WARNING: Destroying ALL Workshop Resources (Starwars, Gateways, ArgoCD, Dashboard)..."
    kubectl delete ns starwars gateways argocd envoy-gateway-system kubernetes-dashboard --ignore-not-found=true
    @echo "🌌 The Galaxy is empty."

# Stop/Clean the Load Test
stop-load:
    kubectl delete job k6-load-test -n starwars --ignore-not-found=true
    kubectl delete configmap k6-script -n starwars --ignore-not-found=true

# --- Logs ---

# Tail Backend Logs
logs-back:
    kubectl logs -n starwars -l component=back -f --tail=100

# Tail Frontend Logs
logs-front:
    kubectl logs -n starwars -l component=front -f --tail=100

# Tail Database Logs
logs-db:
    kubectl logs -n starwars -l component=postgres -f --tail=100

# --- Shell Access ---

# Open shell in Backend Pod
shell-back:
    kubectl exec -it -n starwars deploy/back-deployment -- sh

# Open shell in Frontend Pod
shell-front:
    kubectl exec -it -n starwars deploy/front-deployment -- sh

# Open shell in Database Pod
shell-db:
    kubectl exec -it -n starwars statefulset/postgres-statefulset -- sh
