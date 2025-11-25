# 🎓 Workshop To-Do List

This document outlines the step-by-step progression for the **Jedy-StarWarsKubernetes** workshop.

## ✅ Level 0: Local Development
**Goal:** Run the application components directly on your machine.

- [ ] **Prerequisites:** Python 3.10+, Node.js 20+, Postgres installed.
- [ ] **Database:** Create `star_wars` DB and user.
- [ ] **Backend:** Install requirements, run `uvicorn`.
- [ ] **Frontend:** Install npm packages, run `npm run dev`.
- [ ] **Verify:** App running on localhost.

## ✅ Level 1: Containerization (Docker)
**Goal:** Package applications into containers.

- [ ] **Database:** Run Postgres container with Volume.
- [ ] **Backend:** Write Dockerfile, build image, run container.
- [ ] **Frontend:** Write Dockerfile, build image, run container.
- [ ] **Verify:** App running in containers (manual networking).

## ✅ Level 2: Orchestration (Docker Compose)
**Goal:** Automate multi-container startup.

- [ ] **Compose File:** Create `compose.yaml` (Services: db, back, front).
- [ ] **Launch:** `docker compose up`.
- [ ] **Verify:** All services talking to each other automatically.

## ✅ Level 3: Kubernetes Basics
**Goal:** Deploy to a local Kubernetes cluster.

- [ ] **Cluster:** Enable K8s in Docker Desktop or start Minikube.
- [ ] **Manifests:** Create `postgres.yaml`, `back.yaml`, `front.yaml`.
- [ ] **Deploy:** `kubectl apply -f .`.
- [ ] **Verify:** Pods and Services running (`kubectl get pods`).

## ✅ Level 4: Advanced Networking (Gateway)
**Goal:** Expose app using Gateway API.

- [ ] **Gateway:** Install Envoy Gateway.
- [ ] **Config:** Create GatewayClass and Gateway.
- [ ] **Routes:** Create HTTPRoutes for `/` and `/api`.
- [ ] **Verify:** App accessible via Gateway IP (Port 80).

## ✅ Level 5: Production Grade (SRE)
**Goal:** Resilience and Scaling.

- [ ] **StatefulSet:** Migrate DB to StatefulSet.
- [ ] **Probes:** Add Liveness/Readiness probes.
- [ ] **HPA:** Configure Horizontal Pod Autoscaler.
- [ ] **Stress Test:** Verify scaling under load.