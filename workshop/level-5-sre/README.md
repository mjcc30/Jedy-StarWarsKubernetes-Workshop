# 🎓 Level 5: Production Grade (SRE)

> *"A Jedi uses the Force for knowledge and defense, never for attack."* — Yoda

Welcome to the final trial, Master Jedi. 🧘‍♂️

In **Level 4**, a Gateway you established. Access to the archives, we have.
But a true Jedi Guardian protects the peace. Your infrastructure must be resilient, scalable, and secure.
If a droid crashes, it must restart. If the traffic spikes, more ships you must summon.

**Your Mission:**

1. **Persistence**: Ensure the Database are never lost.
2. **Resilience**: Teach the pods to heal themselves (Probes).
3. **Scalability**: Use the Force to multiply your fleet (HPA).
4. **Configuration**: Separate the codes from the ship (ConfigMaps).

---

## 🛡️ Step 1: The StatefulSet

A `Deployment` is for stateless droids. They are clones.
A Database has identity. Data it holds.
Use a `StatefulSet` we must.

- **Observe**: `postgres.yaml`.
- **Change**: Notice `kind: StatefulSet` and `volumeClaimTemplates`.
- **Effect**: Each pod gets a dedicated Persistent Volume. `postgres-0` is unique.

```bash
kubectl apply -f postgres.yaml
```

---

## ❤️ Step 2: Sensing Life (Probes)

How do you know if a trooper is ready for battle? You check his pulse.
Kubernetes uses **Probes**.

- **Liveness Probe**: "Are you alive?" If no, kill and restart.
- **Readiness Probe**: "Are you ready?" If no, stop sending traffic.

**Inspect** `back.yaml` and `front.yaml`. The probes are defined.

```bash
kubectl apply -f back.yaml
kubectl apply -f front.yaml
```

---

## ⚖️ Step 3: Balance (Autoscaling)

The Force must be balanced. If the Sith attack (high load), we need more Jedi.
**Horizontal Pod Autoscaler (HPA)** does this.

**Prerequisite**: The **Metrics Server** must be running.

```bash
# Install Metrics Server (if not present)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

**Deploy the HPA**:

```bash
kubectl apply -f hpa.yaml
```

Now, if CPU usage goes above 50%, new backend pods will spawn!

---

## 📜 Step 4: The Sacred Texts (Config)

Hardcoding passwords in `back.yaml`... the path to the Dark Side, this is.
We use **ConfigMaps** for settings and **Secrets** for keys.

```bash
kubectl apply -f back-configmap.yaml
kubectl apply -f front-configmap.yaml
```

---

## 🚀 Step 5: The Final Configuration

Ensure all is applied. The Gateway and Routes from Level 4 are still needed.

```bash
# Infrastructure
kubectl apply -f gateway-infra.yaml
kubectl apply -f gatewayclass.yaml

# Routing
kubectl apply -f routes.yaml

# The Dashboard (Optional)
kubectl apply -f dashboard-route.yaml
```

---

## ⚔️ Step 6: Battle Simulation (Load Test)

Does it scale? Test it, we must.

1. **Watch the HPA**:

    ```bash
    kubectl get hpa -n starwars --watch
    ```

2. **Generate Load** (Run this in a new terminal):
    We use a K6 job to flood the API.
    *(Ensure you have the K6 job file or run a temporary pod)*

    ```bash
    # Simulating heavy traffic...
    kubectl run load-generator --image=busybox /bin/sh -- -c "while true; do wget -q -O- http://back-cluster-ip-service:4000/api; done"
    ```

3. **Observe**:
    Watch the `REPLICAS` count increase. The Force is strong!

---

## 🏆 Conclusion

**Rise, Jedi Master.**
You have built a cluster that is:

- **Persistent** (StatefulSet)
- **Self-Healing** (Probes)
- **Elastic** (HPA)
- **Accessible** (Gateway)

The Archives are safe. The Galaxy is at peace.

👉 *May the Force be with you, always.*
