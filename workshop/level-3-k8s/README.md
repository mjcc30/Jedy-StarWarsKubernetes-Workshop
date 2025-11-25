# 🎓 Level 3: Kubernetes Basics (Kubernaut)

> *"In my experience, there is no such thing as luck."* — Obi-Wan Kenobi

Welcome to **Level 3**. You have mastered containers and local orchestration.
Now, we enter the big leagues. **Kubernetes (K8s)**.

Kubernetes is like the Jedi Council for your containers. It manages them, scales them, and heals them.
In this level, we will translate our `compose.yaml` into Kubernetes **Manifests**.

---

## 🛠️ Step 0: Enable Kubernetes

You need a cluster.

- **Docker Desktop**: Kubernetes > Enable Kubernetes.
- **Minikube / Kind**: If you prefer these, start them up.

1. **Open a new terminal**

2. **Check connection:**

```bash
kubectl cluster-info
kubectl get nodes
```

---

In K8s, we don't use one big file. We usually split things up.
We need two main concepts for each app:

1. **Deployment**: Manages the Pods (containers). It handles restarts and updates.
2. **Service**: The stable network address. Even if Pods die and move, the Service IP stays the same.

Navigate to the sector:

```bash

cd workshop/level-3-k8s

```

### 🚀 Step 1: Rebuilding & Updating Images

1. **Rebuild Production Images:**

    ```bash
    # Backend
    docker build -f back/Dockerfile.prod -t jedy-backend:latest back/
    
    # Frontend
    docker build -f front/Dockerfile.prod -t jedy-frontend:latest front/
    ```

## 📜 Step 1: Apply The Manifests

### 1️⃣ The Namespace

```bash
kubectl create ns starwars
```

### 2️⃣ The Database (Postgres)

Check `postgres.yaml`.

- **Deployment**: Runs `postgres:16-alpine`.
- **Service**: Exposes port `5432` internally.

```bash
kubectl apply -f deploy/postgres.yaml
```

### 3️⃣ The Backend

Check `back.yaml`.

- **Deployment**: Runs your `jedy-backend` image.
  - *Important*: `imagePullPolicy: Never` (if using local images in Docker Desktop) or `IfNotPresent`.
  - Env Vars: `DATABASE_URL` should point to `postgres-service` (or whatever you name the service).
- **Service**: Exposes port `4000`.

```bash
kubectl apply -f deploy/back.yaml
```

### 4 The Frontend

Check `front.yaml`.

- **Deployment**: Runs your `jedy-frontend` image.
- **Service**: Exposes port `4321`.
  - *Type*: `LoadBalancer` (to let you access it from your browser easily on localhost).

```bash
kubectl apply -f deploy/front.yaml
```

Now i have all manifest deployed

> *Tip: Or just `kubectl apply -f deploy` or `cd deploy && kubectl apply -f .` to apply everything in the folder* # Use with caution.

---

## 🔍 Step 3: Verification

1. **Check Pods**:
    Are they Running?

    ```bash
    kubectl get pods -n starwars
    ```

2. **Check Services**:

    ```bash
    kubectl get svc -n starwars
    ```

3. **Access the App**:
    - If you used `type: LoadBalancer` for the Frontend, check the `EXTERNAL-IP` (it might be `localhost`).
    - Open `http://localhost:4321`.

**Note on Networking:**
Just like in Level 1, the frontend might load, but **Search** might fail because we haven't set up the Gateway yet (Level 4). The frontend is trying to hit `/api` on its own domain, but K8s handles routing differently.

---

## 🧹 Step 4: Cleanup

To delete the resources:

```bash
kubectl delete -f deploy
```

---

## 🧠 Pods vs Deployments

- **Pod**: The smallest unit. One or more containers. Mortal (they die).
- **Deployment**: The manager. Ensures X number of Pods are always running.

Proceed to Level 4 to fix the networking!
