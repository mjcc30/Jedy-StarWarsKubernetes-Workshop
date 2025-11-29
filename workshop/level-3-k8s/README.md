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
    docker build -f Dockerfile.back.prod -t jedy-backend:latest ../app/back
    
    # Frontend
    docker build -f Dockerfile.front.prod -t jedy-frontend:latest ../app/front
    ```

## 📜 Step 2: Apply The Manifests

### 1️⃣ The Namespace

We create a Namespace (`starwars`) to:

1.  **Isolate**: Separate our Star Wars apps from other things in the cluster.
2.  **Organize**: Group related resources (Pods, Services, PVCs) together.
3.  **Clean up**: `kubectl delete ns starwars` deletes everything inside it instantly.

```bash
kubectl create ns starwars
```

> **Why?**
> A **Namespace** is like a virtual folder within your cluster. It isolates our resources from others.
> Our YAML files (like `back.yaml`) explicitly say `namespace: starwars`. If you don't create it first, Kubernetes will reject the deployment because the destination doesn't exist!

### 2️⃣ The Database (Postgres)

We start with the data.
**Inspect** `postgres.yaml`.

- **Deployment**: Launches the `postgres:16-alpine` container.
- **Service**: Creates a stable internal DNS name (`postgres-service`). Even if the database pod restarts and gets a new IP, the backend can always find it at `postgres-service:5432`.

```bash
kubectl apply -f deploy/postgres.yaml
```

Check deployment:

```bash
kubectl get deploy postgres-deployment -n starwars
```

> **⚠️ Jedi Warning: The Database Dilemma**
> We are using a **Deployment** for the database. For a Jedi Initiate, this is fine.
> But in a real galaxy, this is dangerous! Deployments treat Pods like ephemeral clones. If the Pod dies and moves to another node, the data connection might be lost or corrupted.
> **True Persistence** requires a **StatefulSet**. You will learn this advanced technique in **Level 5**.

### 3️⃣ The Backend

**Inspect** `back.yaml`.

- **Deployment**: Launches your `jedy-backend` image.
  - *Env Vars*: Note how `DATABASE_URL` uses the service name `postgres-service`.
- **Service**: Type `ClusterIP`. This means it is **only** accessible from inside the cluster. It is safe from the outside world (for now).

```bash
kubectl apply -f deploy/back.yaml
```

Check deployment:

```bash
kubectl get deploy back-deployment -n starwars
```

### 4️⃣ The Frontend

**Inspect** `front.yaml`.

- **Deployment**: Launches your `jedy-frontend` image.
- **Service**: Type `ClusterIP`. This means it is **internal only**. Just like the Backend.

```bash
kubectl apply -f deploy/front.yaml
```

Check deployment:

```bash
kubectl get deploy front-deployment -n starwars
```

> *Tip: You can apply all manifests at once with `kubectl apply -f deploy/`.* 

---

## 🔍 Step 3: Verification (The Tunnel)

1. **Check Pods & Services**:

    ```bash
    kubectl get pods -n starwars
    kubectl get svc -n starwars
    ```

    You will see `front-service` has no External IP. If you try to open `localhost` now, it will fail. The Force is trapped inside the cluster.

2. **Open a Tunnel (Port Forward)**:
    We can use `kubectl` to create a temporary portal to the service.

    ```bash
    kubectl port-forward svc/front-service -n starwars 8080:80
    ```

    *(If port 8080 is busy, try a random one like `45678:80`)*

    *Keep this terminal open!*

3. **Access the App**:
   - Open your browser to: **[http://localhost:8080](http://localhost:8080)**.
   - The Archives should load!

4. **Exit port forward**:
   - Press `Ctrl+C` to quit port-forward.

---

## 🌍 Step 4: Exposing to the World (NodePort)

Port forwarding is great for debugging, but we can't keep a terminal open forever.
Let's expose the service permanently on a specific port of the Node.

1. **Edit** `deploy/front.yaml`.
2. **Go to `Frontend Service` section.**
3. **Change** `type: ClusterIP` to `type: NodePort`.
4. **Add** `nodePort: 32766` to the ports section.

**NodePort config (New)**:

```yaml
spec:
  type: NodePort # Expose via NodePort for local access
  selector:
    app: front # Must match the label in the Deployment
  ports:
    - name: http # Name of the port
      protocol: TCP # Protocol used
      port: 80 # Service port
      targetPort: 4321 # Target port on the pod
      nodePort: 32766 # NodePort for accessing the Frontend externally
```

**ClusterIP config (Old)**:

```yaml
spec:
  # ClusterIP is the default. It gives an internal IP.
  # To access it from outside, we will use 'kubectl port-forward'.
  type: ClusterIP 
  selector:
    app: front # Must match the label in the Deployment
  ports:
    - name: http # Name of the port
      protocol: TCP # Protocol used
      port: 4321 # Service port
      targetPort: 4321 # Target port on the pod
```

5. **Apply the Change**:

    ```bash
    kubectl apply -f deploy/front.yaml
    ```

6. **Check Services**:

    ```bash
    kubectl get svc front-service -n starwars
    ```

7. **Verify**:
    - Open **[http://localhost:32766](http://localhost:32766)**.
    - *Note for Minikube/Kubeadm*: Use your Node IP (`kubectl get nodes -o wide`) instead of localhost.

---

## 🛠️ Step 5: The Tools

To truly understand the Force within your Kubernetes cluster, visual tools can be powerful allies. While `kubectl` gives you command, these desktop applications provide a comprehensive overview and interactive control.

- **Headlamp**: An open-source, user-friendly UI for Kubernetes. [Headlamp Website](https://headlamp.dev/)
- **Lens**: Another popular and powerful desktop application for Kubernetes management. [Lens Website](https://k8slens.dev/)

These tools can be particularly helpful for:  

- **Monitoring**: Quickly see the health and status of your applications.
- **Troubleshooting**: Easily access logs and shell into containers.
- **Learning**: Gain a clearer understanding of Kubernetes resources.

---

## ⚖️ Step 6: The Force Multiplication (Scaling & Healing)

A Jedi Master does not fight alone. When the battle intensifies, you must summon reinforcements.

1. **Scale the Backend:**
    Currently, you have 1 backend pod. Let's make it 3.

    ```bash
    kubectl scale deployment back-deployment --replicas=3 -n starwars
    ```

2. **Witness the Arrival:**
    Watch them appear instantly.

    ```bash
    kubectl get pods -n starwars -w
    ```

3. **The Self-Healing Trial:**
    Kubernetes promises that if a pod dies, it will be replaced. Let's test this.
    - Copy the name of one of your backend pods.
    - Open a new terminal.
    - Destroy it!

    ```bash
    kubectl delete pod back-deployment-xxxxxxxxx-xxxxx -n starwars
    ```

    - Watch the list. You will see the old one Terminating and a **new one** ContainerCreating immediately. The Force preserves the balance (3 replicas).

---

## 🔄 Step 7: The Rolling Update

What if we need to upgrade our ship mid-flight? Kubernetes does this with **Rolling Updates**. It replaces pods one by one, so the service never goes down.

1.  **Forge a "V1" Version**:
    Let's pretend we updated the code. We will tag our existing image as `v1`.

    ```bash
    docker tag jedy-backend:latest jedy-backend:v1
    ```

2.  **Trigger the Update**:
    Tell Kubernetes to change the image for the `server` container.

    ```bash
    kubectl set image deployment/back-deployment server=jedy-backend:v1 -n starwars
    ```

3.  **Watch the Rollout**:

    ```bash
    kubectl rollout status deployment/back-deployment -n starwars
    ```

    You will see it updating... 1 old replica down, 1 new replica up... until all are replaced with the `v1` fleet.

4.  **Verify:**
    Check that the image is `v1`.

    ```bash
    kubectl get deployment back-deployment -n starwars -o jsonpath='{.spec.template.spec.containers[0].image}'; echo
    ```
    *Output should be: `jedy-backend:v1`*

---

## ↩️ Step 8: The Undo (Rollback)

1.  **Forge a "V2" Version**:
    Let's pretend we updated the code again.

    ```bash
    docker tag jedy-backend:latest jedy-backend:v2
    ```

2.  **Trigger the Update**:

    ```bash
    kubectl set image deployment/back-deployment server=jedy-backend:v2 -n starwars
    ```

3.  **Watch the Rollout**:

    ```bash
    kubectl rollout status deployment/back-deployment -n starwars
    ```

4.  **Watch the History**:
    See the timeline of your changes.

    ```bash
    kubectl rollout history deployment/back-deployment -n starwars
    ```

    Oh no! The `v2` update had a bug (in our imagination). We must retreat to the previous working version.

5.  **Execute Order 66 (Undo):**

    ```bash
    kubectl rollout undo deployment/back-deployment -n starwars
    ```

6.  **Verify:**
    Check that the image is back to `v1` (or latest). Wait, undo goes back to the *previous* revision (which was v1).

    ```bash
    kubectl get deployment back-deployment -n starwars -o jsonpath='{.spec.template.spec.containers[0].image}'; echo
    ```

    > **🧠 Wisdom: The Timeline**
    > If you check the history again, you might see Revision 1, 3, 4. Where is 2?
    > When you rollback, Kubernetes doesn't turn back time. It takes the configuration from the past (Rev 2) and applies it as a **new** revision (Rev 4).
    > The Force always moves forward, even when we retreat.

---

## 🧹 Step 9: Cleanup

To delete the resources:

```bash
kubectl delete -f deploy
kubectl delete ns starwars
```

---

## 🧠 Pods vs Deployments

- **Pod**: The smallest unit. One or more containers. Mortal (they die).
- **Deployment**: The manager. Ensures X number of Pods are always running.

Proceed to Level 4 to fix the networking!

---

## 🆘 Troubleshooting

### 🔌 Connection Refused / Reset by Peer?

If `kubectl` cannot talk to the cluster (`connection reset by peer` or `server was unable to handle the request`):

1. **Check Docker Desktop**: Ensure the Kubernetes icon is Green (Running). If it's orange or red, restart Docker Desktop.
2. **Context**: Ensure you are using the right context:

   ```bash
   kubectl config use-context docker-desktop
   ```

3. **Reset**: In Docker Desktop Settings > Kubernetes, click "Reset Kubernetes Cluster" if it's stuck. This usually fixes certificate issues.

### 🚫 NodePort Access Failed (Connection Reset)?

If `curl http://localhost:32766` fails with `Connection reset by peer`, Docker Desktop might be struggling to bridge the network.
Bypass the bridge using **Port Forwarding** (as learned in Step 3):

```bash
kubectl port-forward svc/front-service -n starwars 30001:4321
```

Then try accessing **[http://localhost:30001](http://localhost:30001)**. Keep the terminal open!