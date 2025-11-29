# 🎓 Level 5: Production Grade (SRE)

> *"A Jedi uses the Force for knowledge and defense, never for attack."* — Yoda

Welcome to the level 5, Jedi. 🧘‍♂️

In **Level 4**, a Gateway you established. Access to the archives, we have.
But a true Jedi Guardian protects the peace. Your infrastructure must be resilient, scalable, and secure.
If a droid crashes, it must restart. If the traffic spikes, more ships you must summon.

**Your Mission:**

1. **Persistence**: Ensure the Holocrons (Database) are never lost.
2. **Resilience**: Teach the pods to heal themselves (Probes).
3. **Scalability**: Use the Force to multiply your fleet (HPA).
4. **Configuration**: Separate the configuration from the application code (ConfigMaps & Secrets). Change the settings without rebuilding.

**Warning**: If Level 4 resources still exist, conflict they might. Ensure Level 3 and 4 Cleanups are done.

**Navigate to the Sector:**

```bash
cd workshop/level-5-sre
```

---

## 🔐 Step 0: The Keys (Secrets)

Before deploying the fleet, the keys we must forge.
If you deleted the `starwars` namespace, recreate it and the secrets you must.

```bash
# 1. Create Namespace
kubectl create ns starwars

# 2. Create Secrets
kubectl create -n starwars secret generic jwt-secret --from-literal=JWT_SECRET=MyBestSecret
kubectl create -n starwars secret generic pgpassword --from-literal=PGPASSWORD=star_wars_password
# Optional: AI Keys
# kubectl create -n starwars secret generic google-api-key --from-literal=GOOGLE_API_KEY=my_google_key
# kubectl create -n starwars secret generic openrouter-api-key --from-literal=OPENROUTER_API_KEY=my_openrouter_key
```

**Verify the Keys (Decode):**

```bash
kubectl get secret -n starwars
```

To see what is written inside the secret, use this command:

```bash
# Retrieve and decode the Postgres password
kubectl get secret pgpassword -n starwars -o jsonpath="{.data.PGPASSWORD}" | base64 -d; echo
```

> **Explanation:**
>
> - `kubectl get secret ... -o jsonpath="..."`: Extracts just the encoded value string from the JSON object.
> - `| base64 -d`: Pipes that string to the base64 decoder to reveal the human-readable password.

### 💡 Pro Tip: The `.env` Shortcut

Instead of typing every variable manually, you can load them directly from a file:

```bash
# Create a secret from a .env file
# kubectl create secret generic my-secret --from-env-file=.env

# Create a configmap from a .env file
# kubectl create configmap my-config --from-env-file=.config.env
```

### 🧠 Wisdom: True Security (Secret Managers)

**Warning**: Kubernetes Secrets are just Base64 encoded strings stored in the cluster's database (etcd). If someone accesses etcd, they have your passwords.

In a real production galaxy, use a dedicated **Secret Manager** provided by your cloud:

- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Secret Manager**
- **HashiCorp Vault**

These tools encrypt your keys, rotate them automatically, and strictly control access. You then use tools like the **External Secrets Operator** to fetch them securely into your cluster.

---

## 📜 Step 1: The ConfigMaps

The configuration must exist *before* the deployment launch. Otherwise, lost in hyperspace they will be.

```bash
kubectl apply -f deploy/back-configmap.yaml
kubectl apply -f deploy/front-configmap.yaml
```

---

## 🛡️ Step 2: The StatefulSet

In Level 3, we used a `Deployment`. That was risky.
A `Deployment` treats pods like interchangeable clones. If you delete one, another appears, but it has no memory of who it was.

For a Database, identity matters. We use a **StatefulSet**.

- **Stable Network Identity**: The pod is named `postgres-0` (not `postgres-xc9s8`). It is unique.
- **Sticky Storage**: It creates a `PersistentVolumeClaim` that belongs *only* to `postgres-0`. If the pod dies and restarts, it reattaches to the **same disk**. Your data is safe.
- **Ordered Rollout**: It starts and stops pods in strict order (0, then 1, etc.), preventing data corruption during updates.

- **Observe**: `postgres.yaml`.
- **Change**: Notice `kind: StatefulSet` and `volumeClaimTemplates`.

```bash
kubectl apply -f deploy/postgres.yaml
```

**Verify the Database is stable:**

```bash
# Watch the pod start (Ctrl+C to exit)
kubectl get pods -n starwars -w

# Check if the Persistent Volume Claim (PVC) was created
kubectl get pvc -n starwars
```

---

## 🚪 Step 4: The Gateway (Networking)

We must re-establish the Gateway for this new architecture.

**Install the CRDs and Controller:**

```bash
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.6.0 -n envoy-gateway-system --create-namespace
```

*Wait you must, until the pods are ready:*

```bash
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```

**Note for Padawans:** The routes have changed!
In Level 4, we pointed to `back-service` (which might have been NodePort or LoadBalancer).
In Level 5, we point to `back-cluster-ip-service`.

> **Why ClusterIP?**
> This service type restricts access to **internal** traffic only.
>
> - **Security**: The backend cannot be reached directly from the internet (or your laptop's localhost port).
> - **Control**: All traffic MUST pass through the Gateway, which applies our rules (routing, rate limiting, security policies).
> - **Production Standard**: We hide our droids behind the shields.

```bash
# Infrastructure (Gateway Class & Gateway)
kubectl apply -f deploy/gatewayclass.yaml
kubectl apply -f deploy/gateway-infra.yaml

# Routes
kubectl apply -f deploy/routes.yaml
```

---

## ❤️ Step 3: Sensing Life (Apps & Probes)

How do you know if a trooper is ready for battle? You check his pulse.
Kubernetes uses **Probes**.

- **Liveness Probe**: "Are you alive?" If no, kill and restart.
- **Readiness Probe**: "Are you ready?" If no, stop sending traffic.

**Observe the code (added to `back.yaml`):**

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 4000
  initialDelaySeconds: 10 # Wait 10s before first check to let app startup
  periodSeconds: 15       # Check every 15s

readinessProbe:
  httpGet:
    path: /
    port: 4000
  initialDelaySeconds: 5
  periodSeconds: 10
```

**Deploy the fleet:**

```bash
kubectl apply -f deploy/back.yaml
kubectl apply -f deploy/front.yaml
```

**Inspect the Deployment in action:**

```bash
# wait for back deployment
kubectl get deployment back-deployment -n starwars -w

NAME              READY   UP-TO-DATE   AVAILABLE   AGE
back-deployment   0/3     3            0           11s
back-deployment   1/3     3            1           14s
back-deployment   2/3     3            2           16s
back-deployment   3/3     3            3           18s
# `Ctrl+C` -> Exit.

# quick check pods
kubectl get pods -l component=back -n starwars

# If a pod crashes, ask why:
# kubectl describe pod -l component=back -n starwars

# Read the logs to confirm startup:
kubectl logs -l component=back -n starwars --tail=20

INFO:     10.1.0.1:46482 - "GET / HTTP/1.1" 200 OK
```

### 🧪 Testing Auto-Healing (The Jedi Trial)

A true Jedi trusts the Force, but verifies it. Let us test the resilience.

**Trial 1: The Strike (Pod Deletion)**
If a pod is destroyed (by a Sith Lord or a command), the Deployment must replace it.

```bash
# 1. Watch the pods in one terminal
kubectl get pods -n starwars -w

# 2. In another terminal, destroy a backend pod
# (Replace 'back-deployment-xxxx' with your actual pod name)
kubectl delete pod back-deployment-xxxxxxxxx-xxxxx -n starwars
```

**Observation**: Instantaneously, a new pod is created to take its place. This is the **ReplicaSet** controller in action.

**Trial 2: The Internal Failure (Liveness Probe)**
If the application freezes (deadlock), the **Liveness Probe** detects it. Now, with our new Force powers, we can simulate this.

1. **Watch the pods**:
    In one terminal, keep your eyes on the `RESTARTS` column.

    ```bash
    kubectl get pods -n starwars -w
    ```

2. **Trigger the Crash**:
    In another terminal, make the backend unhealthy.
    *(If using Gateway, replace `localhost:80` with your Gateway's IP `127.0.0.1` or `localhost`)*.

    ```bash
    curl -X POST http://localhost/api/simulate/crash
    ```

3. **Wait and Observe (Patience!)**:
    It is not instant. Kubernetes gives the pod a chance to recover.
    - The Liveness Probe checks every 15 seconds.
    - It needs 3 failures to trigger a restart.
    - **Wait about 45 seconds.**
    - Suddenly, you will see `RESTARTS` increment (e.g., `0` -> `1`).
    - The pod has been rebooted by the cluster. **Auto-Healing is active.**

4. **Make it Healthy (Optional)**:
    The new pod starts fresh (healthy), but if you want to be sure:

    ```bash
    curl -X POST http://localhost/api/simulate/heal
    ```

---

## ⚖️ Step 5: Balance (Autoscaling)

The Force must be balanced. If the Sith attack (high load), we need more Jedi.
**Horizontal Pod Autoscaler (HPA)** does this.

**Prerequisite**: The **Metrics Server** must be running.

> **What is the Metrics Server?**
> Think of it as the Force Sense of the cluster.
>
> - It collects resource usage data (CPU, Memory) from every pod.
> - Without it, the HPA is blind; it cannot know if the servers are overloaded.
> - It is not installed by default on many clusters (like Docker Desktop).

```bash
# Install Metrics Server (if not present)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

**Deploy the HPA**:

```bash
kubectl apply -f deploy/hpa.yaml
```

Now, if CPU usage goes above 50%, new backend pods will spawn!

---

## ⚔️ Step 6: Battle Simulation (Load Test)

Does it scale? Test it, we must.

### 1. The Simple Way (Manual Blaster Fire)

For a quick test, we can launch a simple loop from a container inside the cluster.

1. **Watch the HPA**:
    *Run this first so you can see the change happen.*

    ```bash
    kubectl get hpa -n starwars --watch
    ```

    **Wait! `TARGETS: <unknown>/50%`**:
    Initially, you will see `TARGETS: <unknown>/50%`. **This is normal.**
    The Metrics Server needs 1-2 minutes to collect the first data points.
    Do not panic. Wait until you see `0%/50%` or similar.

    **Troubleshooting**: If it stays `<unknown>` for more than 2 minutes, the Metrics Server might need a patch (common in Docker Desktop):

    ```bash
    kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
    ```

    **Then wait again**

2. **Fire the Blasters** (Open Terminal 2):
    *This command runs an infinite loop of requests as fast as possible.*
    *Note: We use `-n starwars` so the pod can find the service (back-cluster-ip-service).*

    ```bash
    kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -n starwars -- /bin/sh -c "while true; do wget -q -O- http://back-cluster-ip-service:4000/ > /dev/null; done"
    ```

3. **Observe**: The CPU usage should rise (e.g., `65%/50%`), and new pods should appear (`REPLICAS: 5`).

    ```bash
    NAME       REFERENCE                    TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
    back-hpa   Deployment/back-deployment   cpu: 2%/50%   1         5         3          5m36s
    back-hpa   Deployment/back-deployment   cpu: 133%/50% 1         5         3          6m21s
    ```

4. **Clean your Blasters**:

    ```bash
    kubectl delete pod load-generator -n starwars
    ```

> **Note:** If you see `TARGETS: <unknown>/50%`, the Metrics Server is not working correctly. Check the **Troubleshooting** section below for the fix.

### 2. The Jedi Way (K6)

The simple loop is like a single stormtrooper. For a real invasion, we use **K6**.

> **Why K6?**
>
> - **Realistic**: Simulates thousands of concurrent users, not just one loop.
> - **Metrics**: Tells you the latency (how slow the site gets) and error rates.
> - **Scenarios**: Can simulate login flows, searching, and browsing simultaneously.

**1. Deploy the Battle Plan (ConfigMap):**

This loads the test script into the cluster.

> **Understanding the Script (`script.js`)**:
>
> - **Stages**: The test simulates a real traffic pattern:
>   - *Warmup*: 30s to reach 20 users.
>   - *Peak Load*: 2 minutes with 100 concurrent users (this triggers HPA).
>   - *Cooldown*: 1 minute to ramp down.
> - **Target**: Hits `http://back-cluster-ip-service:4000/`.
> - **Checks**: Verifies every response is a `200 OK`.

```bash
kubectl apply -f deploy/k6/configmap.yaml
```

**2. Monitor the Results:**

```bash
kubectl get hpa -n starwars --watch
```

**3. Launch the Attack (Job):**
This creates a temporary pod that executes the script.

```bash
cd workshop/level-5-sre/
kubectl apply -f deploy/k6/job.yaml
```

**4. Check the Logs:**
Watch the battle unfold in the logs.

```bash
kubectl logs job/k6-load-test -n starwars -f
```

wait for job test end to get more details about attack

```bash
running (3m39.1s), 004/100 VUs, 71992 complete and 0 interrupted iterations
default   [  99% ] 004/100 VUs  3m28.0s/3m30.0s

running (3m40.1s), 002/100 VUs, 72022 complete and 0 interrupted iterations
default   [ 100% ] 002/100 VUs  3m29.0s/3m30.0s

running (3m41.1s), 001/100 VUs, 72037 complete and 0 interrupted iterations
default   [ 100% ] 001/100 VUs  3m30.0s/3m30.0s


  █ THRESHOLDS 

    http_req_duration
    ✓ 'p(95)<500' p(95)=97.18ms


  █ TOTAL RESULTS

    checks_total.......: 72038   325.702437/s
    checks_succeeded...: 100.00% 72038 out of 72038
    checks_failed......: 0.00%   0 out of 72038

    ✓ status was 200

    HTTP
    http_req_duration..............: avg=48.43ms  min=500.28µs med=5.16ms   max=21.02s p(90)=88.49ms  p(95)=97.18ms
      { expected_response:true }...: avg=48.43ms  min=500.28µs med=5.16ms   max=21.02s p(90)=88.49ms  p(95)=97.18ms
    http_req_failed................: 0.00%  0 out of 72038
    http_reqs......................: 72038  325.702437/s

    EXECUTION
    iteration_duration.............: avg=145.38ms min=100.68ms med=105.86ms max=19.49s p(90)=188.87ms p(95)=197.55ms
    iterations.....................: 72038  325.702437/s
    vus............................: 1      min=1          max=99
    vus_max........................: 100    min=100        max=100

    NETWORK
    data_received..................: 12 MB  54 kB/s
    data_sent......................: 6.1 MB 27 kB/s

running (3m41.2s), 000/100 VUs, 72038 complete and 0 interrupted iterations
default ✓ [ 100% ] 000/100 VUs  3m30s
```

**5. Observe the Aftermath (Cooldown):**
Once the test finishes, the traffic stops.
Keep watching the HPA window. After a few minutes (usually 5m), Kubernetes will scale the fleet back down.

```bash
# You will see REPLICAS drop back to 1
NAME       REFERENCE                    TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
back-hpa   Deployment/back-deployment   cpu: 2%/50%   1         5         3          9m3s
back-hpa   Deployment/back-deployment   cpu: 18%/50%  1         5         3          10m
back-hpa   Deployment/back-deployment   cpu: 69%/50%  1         5         5          11m
back-hpa   Deployment/back-deployment   cpu: 121%/50% 1         5         5          12m
back-hpa   Deployment/back-deployment   cpu: 52%/50%  1         5         5          13m
back-hpa   Deployment/back-deployment   cpu: 2%/50%   1         5         5          14m
```

**6. Cease Fire (Cleanup K6):**
When the battle is over, remove the test runner.

```bash
kubectl delete job k6-load-test -n starwars
kubectl delete configmap k6-script -n starwars
```

---

## 🧹 Step 7: Cleanup

To delete the resources:

```bash
kubectl delete -f deploy
kubectl delete ns starwars
```

## 🏆 Conclusion

**Rise, Jedi Master.**
You have built a cluster that is:

- **Persistent** (StatefulSet)
- **Self-Healing** (Probes)
- **Elastic** (HPA)
- **Accessible** (Gateway)

The Archives are safe. The Galaxy is at peace.

### 📜 The Path to True Production

However, a Jedi's training never ends.
To run this in a real galaxy (AWS/GCP/Azure) with millions of users, you need more. Encryption, GitOps, Observability...

👉 **[Read the PRODUCTION ROADMAP](PRODUCTION_ROADMAP.md)** to see what lies beyond.

👉 *May the Force be with you, always.*

### 🚀 Next Step: The Path of the Master

You have learned the ways of the Jedy SRE. But a true Master does not rely on luck.
To wield the Force with precision, you must equip yourself with the **Jedi Tools**.

👉 **[Proceed to Level 6: The Master's Toolkit](../level-6-mastery/README.md)**

---

## 🆘 Troubleshooting

### 1. HPA shows `<unknown>` CPU

**Symptoms**: `kubectl get hpa` shows `TARGETS: <unknown>/50%`.
**Cause**: The Metrics Server cannot talk to the Kubelet (SSL error).
**Solution**: Patch the metrics server to allow insecure TLS (common in Docker Desktop).

```bash
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
```

> **Explanation of the Patch**:
> This command surgically edits the running Deployment.
>
> - `--type='json'`: Uses JSON Patch to modify a list.
> - `path: .../args/-`: Navigates to the arguments list of the container and appends to the end (`-`).
> - `--kubelet-insecure-tls`: Tells the Metrics Server to skip verifying the SSL certificate of the Node. Necessary for Docker Desktop which uses self-signed certificates.

### 2. Pods crashing / Connection Refused

**Symptoms**: `kubectl describe pod` shows `Readiness probe failed: connect: connection refused`.
**Cause**: The application takes longer to start than the probe waits, or listens on `localhost` instead of `0.0.0.0`.
**Solution**:

- Increase `initialDelaySeconds` in `back.yaml`.
- Ensure your app binds to `0.0.0.0` (Already handled in our Dockerfile).

### 3. Helm Error: "cannot reuse a name"

If `helm install` fails with `cannot reuse a name that is still in use`, it means a previous installation exists (even if failed).

**Solution:**

```bash
helm uninstall eg -n envoy-gateway-system
```

### 4. ImagePullBackOff

If your pods fail with `ImagePullBackOff`, check the image name in your YAMLs.
We use `jedy-backend:latest`. If the YAML says `jedy-starwarskubernetes-back:latest`, it is looking for the wrong ship!
**Solution**: Edit the YAML to match your built image tag.
