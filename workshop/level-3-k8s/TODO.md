# ✅ Level 3 Checklist

Use this list to track your progress as you enter the Kubernetes universe.

- [ ] **Prerequisites**
  - [ ] Kubernetes enabled in Docker Desktop (or Minikube/Kind installed).
  - [ ] `kubectl cluster-info` returns successful connection.
- [ ] **Database Manifests**
  - [ ] `postgres.yaml` created (Deployment + Service).
  - [ ] Applied to cluster: `kubectl apply -f postgres.yaml`.
- [ ] **Backend Manifests**
  - [ ] `back.yaml` created (Deployment + Service).
  - [ ] Applied to cluster: `kubectl apply -f back.yaml`.
- [ ] **Frontend Manifests**
  - [ ] `front.yaml` created (Deployment + Service).
  - [ ] Applied to cluster: `kubectl apply -f front.yaml`.
- [ ] **Verification**
  - [ ] All Pods are Running: `kubectl get pods`.
  - [ ] All Services are created: `kubectl get svc`.
  - [ ] Access via Port-Forwarding (if using ClusterIP) or NodePort.
- [ ] **Cleanup**
  - [ ] Resources deleted: `kubectl delete -f .`.
