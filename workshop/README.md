# 🎓 Workshop: Zero to Hero with Kubernetes

Welcome to the **Jedy-StarWarsKubernetes** workshop. The goal of this course is to take you from a simple application code to a production-grade Kubernetes cluster.

## 📂 Workshop Structure

This folder contains the "Answer Key" for each level of the workshop.

- `level-0-local/`: The Old way.
- `level-1-docker/`: Dockerfiles.
- `level-2-compose/`: Docker Compose configuration.
- `level-3-k8s/`: Simple Kubernetes manifests.
- `level-4-gateway/`: Expose using an API Gateway.
- `level-5-sre/`: The final, production-ready configuration.

---

## Level 0: The Setup (Neophyte)

**Goal**: Run the application locally using language tools.

1. **Backend**:

    ```bash
    cd back
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

2. **Frontend**:

    ```bash
    cd front
    npm install
    npm run dev
    ```

3. **Database**: You need a local Postgres running manually.

---

## Level 1: Containerization (Dockerizer)

**Goal**: Package the application so it runs anywhere.

**Task**: Write a `Dockerfile` for both `back` and `front`.

- **Backend**: Use `python:3.11-slim`, install dependencies, expose port 4000.
- **Frontend**: Use `node:20-alpine`, build the Astro app, expose port 4321.

👉 *Solution: `level-1-docker/`*

---

## Level 2: Orchestration (Composer)

**Goal**: Connect the containers together easily.

**Task**: Write a `compose.yaml` file.

- Define 3 services: `database`, `back`, `front`.
- Use `depends_on` to manage startup order.
- Connect them using Environment Variables (`DATABASE_URL`).

👉 *Solution: `level-2-compose/`*

---

## Level 3: Kubernetes Basics (Kubernaut)

**Goal**: Move from Docker Compose to Kubernetes manifests.

**Task**: Translate your Compose file into K8s YAMLs.

- Create 3 Deployments (`back`, `front`, `postgres`).
- Create 3 Services to expose them internally (`ClusterIP`) or externally (`NodePort`).
- Apply them using `kubectl apply -f .`.

👉 *Solution: `level-3-k8s/`*

---

## Level 4: Advanced Networking (Architect)

**Goal**: Expose your app properly using an API Gateway (Ingress).

**Task**:

- Install **Envoy Gateway**.
- Create a `Gateway` resource listening on port 80.
- Create `HTTPRoute` resources to route `/api` to the backend and `/` to the frontend.

👉 *Solution: `level-4-gateway/`*

---

## Level 5: Production Grade (SRE)

**Goal**: Make the cluster robust, self-healing, and scalable.

**Task**:

1. **StatefulSet**: Migrate Postgres Deployment to a StatefulSet for data safety.
2. **Probes**: Add `livenessProbe` and `readinessProbe` to handle crashes and rolling updates without downtime.
3. **Autoscaling**: Install Metrics Server and configure `HorizontalPodAutoscaler` (HPA).
4. **Load Test**: Stress test the app to see it scale.

👉 *Solution: `level-5-sre/`*

---

## 🛠 Tools

Use the provided `Justfile` (at the root of the repo) to help you run common commands if you get stuck.
