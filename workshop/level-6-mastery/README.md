# 🎓 Level 6: The Master's Toolkit

> *"Always more to learn, there is."* — Yoda

Welcome to the final level, Master. 🧘‍♂️

You have built a resilient, scalable production cluster. But a true Master does not struggle with raw YAMLs and manual commands daily. They use **Tools** to extend their perception and speed.

**Your Mission:**

1. **Visualize** the Force with the **Kubernetes Dashboard**.
2. **Navigate** the Matrix with **K9s**.
3. **Switch** contexts instantly with **kubectx**.

---

## 📊 Step 1: The Visualizer (Kubernetes Dashboard)

A Graphical User Interface (GUI) to see your Deployments, Pods, and HPA graphs.

### 1. Install the Dashboard

We use Helm to install the official dashboard.

```bash
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard \
  --set kong.proxy.http.enabled=true \
  --set kong.proxy.http.servicePort=80 \
  --set kong.proxy.http.containerPort=8000 
```

### 2. Expose it (Gateway)

We route `http://localhost/dashboard` to the dashboard service.

```bash
kubectl apply -f dashboard-route.yaml
```

### 3. Grant Access (Admin User)

The dashboard is secure by default. We need a Service Account with permissions.

```bash
kubectl apply -f dashboard-admin.yaml
```

### 4. Generate the Key

Create a temporary token to log in.

```bash
kubectl -n kubernetes-dashboard create token admin-user
```

**Action:**

1. Copy the token.
2. Go to [http://localhost/dashboard](http://localhost/dashboard).
3. Paste the token.
4. Explore your `starwars` namespace!

---

## 🐶 Step 2: The Terminal Companion (K9s)

`kubectl` is powerful, but verbose. **K9s** is a terminal-based UI that lets you navigate your cluster like a starfighter pilot.

**Install K9s:**

- **Mac**: `brew install derailed/k9s/k9s`
- **Windows**: `choco install k9s`
- **Linux**: [Check releases](https://github.com/derailed/k9s)

**Launch:**

```bash
k9s
```

**Master Keys:**

- `:ns` -> Select Namespace (choose `starwars`).
- `:pod` -> View Pods.
- `l` -> Logs (on a selected pod).
- `s` -> Shell (exec into a pod).
- `d` -> Describe.
- `Ctrl+C` -> Exit.

---

## ⚡ Step 3: The Context Switcher (kubectx & kubens)

When you manage multiple clusters (Dev, Prod) or namespaces, typing `-n starwars` every time leads to the Dark Side (Carpal Tunnel).

**Install:**

- **Mac**: `brew install kubectx`
- **Windows**: `choco install kubens`

**Usage:**

```bash
# Switch default namespace to starwars
cubens starwars

# Now you can just type:
kubectl get pods
# Instead of:
kubectl get pods -n starwars
```

---

## 🏆 Conclusion

You are now fully equipped.

- You have the **Knowledge** (K8s Architecture).
- You have the **Infrastructure** (Gateway, HPA).
- You have the **Tools** (Dashboard, K9s).

**The Galaxy is yours to protect.**

👉 *This is the way.*
