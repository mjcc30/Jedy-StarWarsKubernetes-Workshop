# 🎓 Level 6: The Master's Toolkit

> *"Always more to learn, there is."* — Yoda

Welcome to the level 5, Master. 🧘‍♂️

You have built a resilient, scalable production cluster. But a true Master does not struggle with raw YAMLs and manual commands daily. They use **Tools** to extend their perception and speed.

**Your Mission:**

1. **Visualize** the Force with the **Kubernetes Dashboard**.
2. **Navigate** the Matrix with **K9s**.
3. **Switch** contexts instantly with **kubectx**.

---

## 🛠️ Step 0: Prerequisite (The Gateway)

To access the Dashboard, we rely on the Gateway you built in previous levels.
If you cleaned up (destroyed) your cluster after Level 5, you must restore the Gateway Infrastructure.

```bash
# 1. Install Envoy Gateway Controller
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.6.0 -n envoy-gateway-system --create-namespace

# 2. Deploy Gateway Infrastructure (using Level 5 files)
kubectl apply -f ../level-5-sre/deploy/gatewayclass.yaml
kubectl apply -f ../level-5-sre/deploy/gateway-infra.yaml
```

*Wait for the Gateway IP (`127.0.0.1`) to appear:* `kubectl get gateway -n gateways`.

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

# We can see this output but skip this instruction:
Congratulations! You have just installed Kubernetes Dashboard in your cluster.

To access Dashboard run:
  kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

NOTE: In case port-forward command does not work, make sure that kong service name is correct.
      Check the services in Kubernetes Dashboard namespace using:
        kubectl -n kubernetes-dashboard get svc

Dashboard will be available at:
  https://localhost:8443
```

### 2. Expose it (Gateway)

We route `http://localhost/dashboard` to the dashboard service.

```bash
cd workshop/level-6-mastery
kubectl apply -f deploy/dashboard-route.yaml
```

### 3. Grant Access (Admin User)

The dashboard is secure by default. We need a Service Account with permissions.

```bash
kubectl apply -f deploy/dashboard-admin.yaml
```

### 4. Generate the Key

Create a temporary token to log in.

```bash
kubectl -n kubernetes-dashboard create token admin-user

# output:
eyJhbGciOiJSUzI1NiIsImtpZCI6InNISzAxOFZ0QlAydWR3T0psbWRFdm12WVVHUTd2SHdBYV9UQTFwS3Rod2sifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzY0NDI2Nzk5LCJpYXQiOjE3NjQ0MjMxOTksImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiMjJjY2ZjNzUtMjMyOS00ZDg0LWE1MWMtMDZhZmFlZWJkMGYwIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJhZG1pbi11c2VyIiwidWlkIjoiMjE5ODJiZjItMTkwNi00NTRjLTk2OTctMzRkOWE1ZGIxNTVkIn19LCJuYmYiOjE3NjQ0MjMxOTksInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDphZG1pbi11c2VyIn0.RugcLRN47OOccGm6ER5QF32GmkYtTIMF1594qUDesx-tZPPnk4Ns_QMjtYO8CULHtnj7N0Nh0NWI6HmHgQJZuOF4X-eikjCz89BQY4rczX3awB-i7pddpbKJoFD9c9wAUTXYY-V6Uosv_QGLg-IR7nI8CbrwWFhYtWtfRfXhvMHnUKZwG6GO8kUY5A-GFrugFHEY0w2yf5ewTP4diar8_mErduV8MfEe8LeJBh53s-OSQCkzf-NLMBsSMkZ-vW0OOxzh5BoI1wnL_pUuIwv6Y5wtJ7hMilFetdciSWF8ZdNM0Z7rlz4kFrF6HhB4NUpfT35DqTLcO6QNGxuIndHX0g
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

- **Mac\Linux\WSL**: `brew install derailed/k9s/k9s`
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

- **Mac\Linux\WSL**: `brew install kubectx`
- **Windows**: `choco install kubens`

**Usage:**

```bash
# Switch default namespace to starwars
kubens starwars

# Now you can just type:
kubectl get pods
# Instead of:
kubectl get pods -n starwars
```

---

## 📜 Step 4: The Log Hunter (Stern)

`kubectl logs` is limited. **Stern** allows you to tail multiple pods and containers simultaneously, with color-coded output.

**Install:**

- **Mac\Linux\WSL**: `brew install stern`
- **Windows**: `choco install stern`
- **Linux**: [Check releases](https://github.com/stern/stern)

**Usage:**
Tail all pods in the `starwars` namespace:

```bash
stern -n starwars .
```

Tail only the backend pods:

```bash
stern -n starwars back
```

Tail only the frontend pods:

```bash
stern -n starwars front
```

---

## 🩺 Step 5: The Cluster Sanitizer (Popeye)

A Jedi keeps their ship clean. **Popeye** scans your cluster for misconfigurations (missing probes, resource limits, etc.) and gives you a score.

**Install:**

- **Mac\Linux\WSL**: `brew install derailed/popeye/popeye`
- **Windows**: `choco install popeye`
- **Linux\WSL**: [Check releases](https://github.com/derailed/popeye)

**Scan:**

```bash
popeye -n starwars
```

### 🧠 Understanding Popeye's Judgment

You might see a score of **B** or **C**. Do not fear! Popeye is strict. It highlights best practices we skipped for simplicity.

The output highlights Best Practices that are missing.
It flags them as 😱 (Error/Critical) or 🔊 (Warning).

The Main Issues & Why they matter:

  1. [POP-101] Image tagged "latest" in use (😱)
      - Where: back-deployment & front-deployment.
      - Why: Using :latest is dangerous in production. You never know exactly which version is running. If you deploy today and tomorrow, you might get different code.
      - Fix: Use specific tags like :v1.0.0 or :sha256:....

  2. [POP-306] Container could be running as root user (😱)
      - Where: All pods (back, front, postgres).
      - Why: Security! If a hacker breaks into the container, they are Root. They might escape to the Node.
      - Fix: Add securityContext: runAsNonRoot: true and runAsUser: 1000 in the YAML.

  3. [POP-1204] Pod ingress/egress is not secured by a network policy (😱)
      - Where: All pods.
      - Why: Zero Trust. By default, any pod can talk to any pod. If the Frontend is compromised, it can attack the Database directly.
      - Fix: Create NetworkPolicy to allow only specific traffic (Front -> Back -> DB).

  4. [POP-106] No resources requests/limits defined (😱)
      - Where: wait-for-postgres (init container).
      - Why: Neighbors. A pod without limits can eat all CPU/Memory on the node, crashing other pods.
      - Fix: Add resources: section to the init container.

  5. [POP-300] Uses "default" ServiceAccount (😱)
      - Where: All pods.
      - Why: The default SA often has (or is assumed to have) permissions. Best practice is to create a dedicated ServiceAccount for each app with minimal permissions.

  6. [POP-108] Unnamed port (🔊)
      - Where: Services/Pods.
      - Why: Clarity. Referring to ports by name (http, postgres) is safer than numbers (80, 5432).

Lesson for the Padawan:
"A working cluster is not always a good cluster. Popeye reveals the invisible cracks in your armor. To reach Level 7
(Grandmaster), you would fix these."

👉 *To fix these, you would follow the [Production Roadmap](../level-5-sre/PRODUCTION_ROADMAP.md).*

---

## ⚡ Step 6: Force Speed (Aliases)

Typing `kubectl` takes too long. A Master uses shorthand.

**Add to your shell profile (`nano ~\.bashrc` or `nano ~\.zshrc`):**

```bash
alias k=kubectl
alias kg="kubectl get"
alias kd="kubectl describe"
alias kdel="kubectl delete"
alias klogs="kubectl logs"
```

**Usage:**

```bash
k get pods
klogs -f my-pod
```

---

## 🚀 Master's Tools: Just a Jedi Master

A true Master works efficiently. To speed up your training, we have provided a **Holocron of Shortcuts** (a `Justfile`).

It is located at the **root of the repository** (`/Jedy-StarWarsKubernetes-Workshop/Justfile`). It aggregates the commands you learned in all previous levels into simple shortcuts.

**Inspect the Holocron:**

```bash
cat ../../Justfile
```

**1. Install `just`:**

- **MacOS**: `brew install just`
- **Windows**: `winget install casey.just` or `choco install just`
- **Linux**: Check your package manager or [install from source](https://github.com/casey/just).

**2. Use the Force:**

You can run these commands from **anywhere** inside the project folder. `just` is smart enough to find the Holocron at the root.

- **`just dev`**: Launches the local development stack (Level 2).
- **`just down`**: Stops all Docker Compose containers.
- **`just deploy`**: Deploys the full production stack to Kubernetes (Level 5).
- **`just undeploy`**: Removes all Kubernetes resources.
- **`just load-test`**: Runs the K6 battle simulation.
- **`just`**: (Type `just` alone to see all available commands.)

👉 *Learn more about this powerful tool: [https://github.com/casey/just](https://github.com/casey/just)*

---

## 📚 The Holocron of Knowledge

Even a Master must continue to learn.
If you seek further wisdom in the French language, consult the archives of **Master Stéphane Robert**.

👉 **[blog.stephane-robert.info](https://blog.stephane-robert.info/docs/)**

He teaches the ways of:

- **Kustomize**: An alternative to Helm for managing configuration overlays.
- **Sealed Secrets**: Encrypting secrets so they can be stored in Git.
- **DevSecOps**: Securing the galaxy supply chain.

---

## 🏆 Conclusion

You are now fully equipped.

- You have the **Knowledge** (K8s Architecture).
- You have the **Infrastructure** (Gateway, HPA).
- You have the **Tools** (Dashboard, K9s).

**The Galaxy is yours to protect.**

👉 *This is the way.*

---

### 🚀 The Final Trial

**Afraid of the Dark Side (Manual Deployments), are you?**
Then you must master the Automator.

👉 **[Proceed to Level 7: The Automator (GitOps)](../level-7-gitops/README.md)**
