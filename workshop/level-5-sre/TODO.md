# ✅ Level 5 Checklist

Use this list to track your progress as you build a Production-Grade Cluster.

- [ ] **Data Persistence (StatefulSet)**
  - [ ] Migrate Postgres from Deployment to `StatefulSet`.
  - [ ] Verify `volumeClaimTemplates` are creating PVCs.
- [ ] **Resilience (Probes)**
  - [ ] Add `livenessProbe` to Backend/Frontend.
  - [ ] Add `readinessProbe` to Backend/Frontend.
  - [ ] Verify failing pods are restarted automatically.
- [ ] **Scalability (HPA)**
  - [ ] Install Metrics Server.
  - [ ] Create `hpa.yaml` for Backend.
  - [ ] Generate load and observe scaling: `kubectl get hpa -w`.
- [ ] **Config Management**
  - [ ] Move environment variables to `ConfigMap` and `Secret`.
  - [ ] Update Deployments to reference these resources.
