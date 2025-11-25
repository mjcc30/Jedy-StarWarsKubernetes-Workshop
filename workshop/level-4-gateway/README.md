# 🎓 Level 4: Advanced Networking (Architect)

> *"The Force binds the galaxy together."* — Yoda

Welcome, Architect. 🏗️

In **Level 3**, our Pods were flying, but isolated. The Frontend could not talk to the Backend properly.
To bring balance, we must establish a **Gateway**. A single entry point, managing all traffic, routing requests like a Jedi redirects blaster bolts.

**Your Mission:**

1. **Install** the Gateway Controller (Envoy).
2. **Define** the Class and Infrastructure (`Gateway`).
3. **Map** the routes (`HTTPRoute`).

---

## 🛠️ Step 0: The Tooling (Install Helm)

To command the cluster efficiently, a package manager you need. [Helm](https://helm.sh/docs/intro/install/), it is called. Like a droid for your deployments, it is.

- **Windows**: `choco install kubernetes-helm` or `winget install Helm.Helm`
- **Mac**: `brew install helm`
- **Linux**:

  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  ```

**Verify the installation:**

```bash
helm version
```

---

## 🚪 Step 1: The Gatekeeper (Install Envoy)

Kubernetes has a standard for this: the **Gateway API**. But we need an implementation. We use **Envoy Gateway**.

**Install the CRDs and Controller:**

```bash
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.6.0 -n envoy-gateway-system --create-namespace
```

*Wait you must, until the pods are ready:*

```bash
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```

---

## 🏛️ Step 2: The Foundation (Gateway Infra)

We must tell the cluster "Here is a Gateway".

**Inspect** `gatewayclass.yaml` and `gateway-infra.yaml`.

- **GatewayClass**: Defines *who* manages the gateway (Envoy).
- **Gateway**: The actual listener (Port 80).

1. **Open a terminal, you must.**

2. **Verify the connection:**

    ```bash
    kubectl cluster-info
    kubectl get nodes
    ```

3. **Navigate to the level:**

    ```bash
    cd workshop/level-3-k8s
    ```

**Apply them:**

```bash
kubectl apply -f gatewayclass.yaml
kubectl apply -f gateway-infra.yaml
```

---

## 🗺️ Step 3: The Star Charts (Routes)

Now, the traffic flows to the Gateway. But where does it go?
We need **HTTPRoutes** to direct the ships.

**Inspect** `routes.yaml`.

- **`/api`**: Goes to `back-service`. Note the **URLRewrite**! It strips `/api` so the backend receives `/users` instead of `/api/users`.
- **`/`**: Goes to `front-service`.

**Apply the routes:**

```bash
kubectl apply -f routes.yaml
```

---

## 📡 Step 4: Communication (Verification)

1. **Find the IP**:
    The Gateway creates a LoadBalancer service.

    ```bash
    kubectl get gateway -n gateways
    ```

    *(If using Docker Desktop, it is `localhost`)*.

2. **Test the Archives**:
    Open your browser: [http://localhost](http://localhost).

    - The Frontend should load.
    - Try to **Login** or **Search**.
    - It works! The Gateway is routing `/api` requests to the Python backend correctly.

---

## 🧹 Step 5: Cleanup

When ready to move to the final level:

```bash
kubectl delete -f .
```

Delete the Gateway API CRDs and Envoy Gateway:

```bash
helm uninstall eg -n envoy-gateway-system
```

**Proceed now to Level 5. The final test of a Site Reliability Engineer (SRE) awaits.**
