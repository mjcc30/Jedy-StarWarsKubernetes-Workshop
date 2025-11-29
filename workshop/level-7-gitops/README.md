# 🎓 Level 7: GitOps (The Automator)

> *"Everything is proceeding as I have foreseen."* — The Emperor

Welcome to the final trial.
Here, we stop typing `kubectl apply`. We let the robots do the work.

**Your Mission:**
Build a **GitOps** pipeline where the cluster synchronizes itself with the code.

---

## 🧹 Step 0: The Great Purge

We must start with a clean slate. Destroy the old ways.

```bash
kubectl delete ns starwars argocd gateways envoy-gateway-system --ignore-not-found=true
```

---

## 🐙 Step 1: Install ArgoCD (Bootstrap)

We start by installing the GitOps controller manually (the "Bootstrap").

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace
```

---

## 🔮 Step 2: First Contact (Port Forward)

Before we set up the Gateway, let's ensure ArgoCD is alive.

1. **Get the Password:**

    ```bash
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
    ```

2. **Open the Tunnel:**

    ```bash
    kubectl port-forward svc/argocd-server -n argocd 8080:443
    ```

3. **Login:**

    - Go to [https://localhost:8080](https://localhost:8080).
    - Username: `admin`
    - Password: (The one you copied).
    - *Note: Accept the self-signed certificate warning.*

---

## 🚪 Step 3: Install Infrastructure (Envoy via ArgoCD)

Now, we use ArgoCD to install our Gateway.

1. **Apply the App Manifest:**

    ```bash
    kubectl apply -f argocd-envoy-app.yaml
    ```

2. **Watch it Sync:**
    - Check [argocd applications](https://localhost:8080/applications) if you want to watch in UI.
    - Port-forward again if you did `Ctrl+C`.
    - Or watch pods: `kubectl get pods -n envoy-gateway-system -w`.

---

## 🏗️ Step 3.5: Initialize the Gateway

ArgoCD installed the *software* (Envoy Controller), but we need to define the *infrastructure* (LoadBalancer).

```bash
kubectl apply -f ../level-5-sre/deploy/gatewayclass.yaml
kubectl apply -f ../level-5-sre/deploy/gateway-infra.yaml
```

*Wait for the IP:* `kubectl get gateway -n gateways` (Should show `127.0.0.1`).

---

## ⚡ Step 4: The Upgrade (Self-Management)

We want to access ArgoCD via the Gateway (`http://localhost/argocd`) without port-forwarding.
We need to configure ArgoCD to run in **Insecure Mode** (HTTP) and serve under `/argocd`.

**Upgrade using Helm:**

```bash
helm upgrade argocd argo/argo-cd -n argocd -f argocd-values.yaml
```

*Wait for the `argocd-server` pod to restart.*

```bash
# Command to watch the restart:
kubectl rollout status deployment/argocd-server -n argocd -w
# Or simply watch the pods:
kubectl get pods -n argocd -w
```

---

## 📡 Step 5: Access via Gateway

Now that Envoy is running and ArgoCD is configured:

1. **Check Gateway IP:**

    ```bash
    kubectl get gateway -n gateways
    ```

    *(Wait for `127.0.0.1`)*.

2. **Access:**
    - Go to [http://localhost/argocd](http://localhost/argocd).
    - You should see the login page (no SSL warning this time!).

---

## 🚀 Step 6: Deploy the Fleet (The Jedy App)

Finally, we deploy our Star Wars stack using GitOps.

1. **Configure the Repo:**
    - Edit `argocd-app.yaml`.
    - Change `repoURL` to **YOUR FORK**.

2. **Apply the App:**

    ```bash
    kubectl apply -f argocd-starwars-app.yaml
    ```

3. **Verify:**
    - Check ArgoCD UI. You should see `starwars-app` syncing.
    - Go to [starwars-app](http://localhost/argocd/applications/argocd/starwars-app).
    - Wait for sync 
    - Check the app: [http://localhost](http://localhost) (Frontend).

---

## 💥 Step 7: The Resilience Test

GitOps ensures the cluster always matches Git. If we delete something manually, ArgoCD should fix it.

1.  **Destroy the App:**
    ```bash
    kubectl delete deployment back-deployment -n starwars
    ```

2.  **Watch the Resurrection:**
    - Go to ArgoCD UI.
    - It might say "OutOfSync".
    - Click **Sync** (or wait for auto-sync if enabled).
    - The deployment reappears!

**You have mastered the Loop.**

---

## 🏆 Final Victory

You have traversed the path from **Local Code** -> **Docker** -> **Kubernetes** -> **Gateway** -> **SRE** -> **GitOps**.

You are no longer a Padawan.
**Rise, Jedi Master.**