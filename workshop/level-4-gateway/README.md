# 🎓 Level 4: Advanced Networking (Architect)

> *"The Force binds the galaxy together."* — Yoda

Welcome, Architect. 🏗️

In **Level 3**, our Pods were flying, but isolated. The Frontend could not talk to the Backend properly.
To bring balance, we must establish a **Gateway**. A single entry point, managing all traffic, routing requests like a Jedi redirects blaster bolts.

**Your Mission:**

1. **Install** the Gateway Controller (Envoy).
2. **Define** the Class and Infrastructure (`Gateway`).
3. **Map** the routes (`HTTPRoute`).

### 🧠 Wisdom: Why use a Gateway?

You might ask: *"Master, NodePort worked. Why complicate things?"*

1. **Single Entrypoint**: Instead of opening 10 different ports (30000, 30001...) for 10 services, we use **Port 80** for everything.
2. **Smart Routing**: The Gateway reads the URL. It sends `/api` to the backend and `/` to the frontend. NodePort cannot do this.
3. **Security**: We hide our services deep inside the cluster (ClusterIP). Only the Gateway stands at the door.

---

## 🛠️ Step 0: The Tooling

To command the cluster efficiently, a package manager you need. [Helm](https://helm.sh/docs/intro/install/), it is called. Like a droid for your deployments, it is.

### 1. Install Homebrew (Linux/WSL)

For Linux and Windows Subsystem for Linux (WSL), **Homebrew** is a powerful crossplateform package manager, a true ally for installing development tools.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Next steps you must take:**

- **Run these commands in your terminal to add Homebrew to your PATH:**

  ```bash
  echo >> /home/$USER/.bashrc
  echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/$USER/.bashrc
  eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
  ```

- **Install Homebrew's dependencies (if you have sudo access):**

  ```bash
  sudo apt-get install build-essential
  ```

  For more information, consult: [Homebrew-on-Linux documentation](https://docs.brew.sh/Homebrew-on-Linux)

- **We recommend that you install GCC (if needed):**

  ```bash
  brew install gcc
  ```

- **Verify Homebrew:**

  ```bash
  brew help
  ```

  Further wisdom: [Homebrew documentation](https://docs.brew.sh)

### 2. Install Helm

- **Windows**: `choco install kubernetes-helm` or `winget install Helm.Helm`
- **Mac**: `brew install helm`
- **Linux**: (If you didn't use Homebrew, or prefer direct install)

  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  ```

**Verify your Helm installation:**

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

## 🚀 Step 2: Deploy the Fleet

Before we route traffic, we need destinations. We must deploy our Star Wars applications again (or ensure they are running).

1. **Create Namespace**:

    ```bash
    kubectl create ns starwars
    ```

2. **Deploy Apps**:
    Apply the backend, frontend, and database.

    ```bash
    kubectl apply -f deploy/postgres.yaml
    kubectl apply -f deploy/back.yaml
    kubectl apply -f deploy/front.yaml
    ```

---

## 🏛️ Step 3: The Foundation (Gateway Infra)

We must tell the cluster "Here is a Gateway".

**Inspect** `gatewayclass.yaml` and `gateway-infra.yaml`.

- **GatewayClass**: This defines **WHO** creates the gateway. We point to `eg` (Envoy Gateway). Think of it as choosing the contractor who builds the spaceport.
- **Gateway**: This defines **WHERE** and **HOW** we listen. It requests an External IP (LoadBalancer) and listens on Port 80.

1. **Verify the connection:**

    ```bash
    kubectl cluster-info
    kubectl get nodes
    ```

2. **Navigate to the level:**

    ```bash
    cd workshop/level-4-gateway/deploy
    ```

**Apply them:**

```bash
kubectl apply -f gatewayclass.yaml
kubectl apply -f gateway-infra.yaml
```

> **Why Port 80?**
> In Level 3, we accessed the app via port `30000` (NodePort). Why? Because NodePorts are restricted to high numbers.
> In Level 4, the Gateway creates a **LoadBalancer**. This prompts the infrastructure (Docker Desktop or Cloud Provider) to assign a "Real" IP address and allows us to use the standard web port: **80**. No more ugly port numbers in the URL!

---

## 🗺️ Step 4: The Star Charts (Routes)

Now, the traffic flows to the Gateway (Port 80). But where does it go?
We need **HTTPRoutes** to map URL paths to our Services (ClusterIPs).

**Inspect** `routes.yaml`.

- **Route `/api` -> `back-service`**:
  - We catch everything starting with `/api`.
  - **URLRewrite**: Crucial! The user asks for `/api/users`. The Backend expects `/users`. This filter strips the `/api` prefix before forwarding the request.
- **Route `/` -> `front-service`**:
  - All other traffic goes to the Frontend.

**Apply the routes:**

```bash
kubectl apply -f deploy/routes.yaml
```

---

## 📡 Step 4: Communication (Verification)

1. **Find the IP**:
    The Gateway creates a LoadBalancer service.

    ```bash
    kubectl get gateway -n gateways
    ```

    *(If using Docker Desktop, it is `localhost` or `127.0.0.1`)*.

2. **Test the Routing**:
    Open your browser or use `curl`.

    - **Frontend (Root)**: [http://localhost](http://localhost)
      - *Result*: You should see the Star Wars Archives.
    - **Backend (API)**: [http://localhost/api/](http://localhost/api/)
      - *Result*: `{"message":"Welcome to the Star Wars API"}`

    **The Lesson**: Two different applications, served on the **same port (80)**, routed by path. This is the power of the Gateway.

3. **Try the App**:
    - Go to [http://localhost](http://localhost).
    - Try to **Search**.
    - It works! The Frontend code calls `/api/...`, and the Gateway correctly routes it to the Backend.

---

## 🌟 Advanced Capabilities

We only scratched the surface. **Envoy Gateway** can do much more than simple routing:

- **Traffic Splitting**: Send 90% of traffic to v1 and 10% to v2 (Canary Testing).
- **Rate Limiting**: Protect your API from being overwhelmed (e.g., 100 req/min).
- **Authentication**: Check JWT tokens or OAuth before letting traffic in.
- **TLS Termination**: Handle HTTPS certificates automatically.

👉 **Explore the Archives**: [Envoy Gateway Documentation](https://gateway.envoyproxy.io/docs/)

---

## 🏆 Bonus Level: The Canary Release

Ready for a challenge? Let's split the traffic between two versions of the backend (v1 and v2), sending 90% to v1 and 10% to v2.

1. **Prepare the Image**:
    Ensure you have the `v2` tag (from Level 3). If not:
  
    ```bash
    docker tag jedy-backend:latest jedy-backend:v2
    ```

2. **Deploy Backend V2**:
    This creates a second Deployment and Service (`back-v2-service`).

    ```bash
    kubectl apply -f deploy/bonus-canary/back-v2.yaml
    ```

3. **Split the Traffic**:
    Apply a new Route that overwrites the old one.

    ```bash
    kubectl apply -f deploy/bonus-canary/canary-route.yaml
    ```

4. **Test It**:

    Send many requests. Watch the response message switch between v1 and v2!

    ```bash
    for i in {1..20}; do curl -s http://localhost/api/ | grep message; done
    ```

    *Output:*

    ```json
    {"message":"Welcome to the Star Wars API v1"}
    {"message":"Welcome to the Star Wars API v1"}
    {"message":"Welcome to the Star Wars API v2"}  <-- The Canary!
    {"message":"Welcome to the Star Wars API v1"}
    ...
    ```

5. **Shift Power (50/50)**:

    v2 looks good? Let's increase the load.

    - Edit `deploy/bonus-canary/canary-route.yaml`.
    - Set weights to `50` for v1 and `50` for v2.
    - Apply. Now half the galaxy uses the new system.

6. **The Cutover (100%)**:

    Victory is assured. Move 100% of traffic.

    - Edit weights to `0` for v1 and `100` for v2.
    - Apply.
    - Now v1 is silent. You can safely delete the old deployment later.

---

## 🧹 Step 6: Cleanup

When ready to move to the final level:

```bash
kubectl delete -f deploy/bonus-canary
kubectl delete -f deploy
kubectl delete ns starwars
```

Delete the Gateway API CRDs and Envoy Gateway:

```bash
helm uninstall eg -n envoy-gateway-system
```

**Proceed now to Level 5. The final test of a Site Reliability Engineer (SRE) awaits.**

---

## 🆘 Troubleshooting

### 🛑 Helm Error: "cannot reuse a name"

If you try to install and get: `Error: INSTALLATION FAILED: cannot reuse a name that is still in use`, it means the previous installation wasn't cleaned up properly.

1. **Check status**:

    ```bash
    helm list -A
    ```

2. **Uninstall**:

    ```bash
    helm uninstall eg -n envoy-gateway-system
    ```

### ⏳ Gateway Address is Pending

If `kubectl get gateway -n gateways` shows empty `ADDRESS` or `PROGRAMMED: False` for a long time:

1. **Wait**: It can take 2-3 minutes on a slow machine.
2. **Check Controller**:

    ```bash
    kubectl get pods -n envoy-gateway-system
    ```

    If the controller pod is crashing, check logs: `kubectl logs -n envoy-gateway-system -l control-plane=envoy-gateway`.
3. **Docker Desktop**: Ensure "Enable Kubernetes" is checked and working. The LoadBalancer feature depends on it.
