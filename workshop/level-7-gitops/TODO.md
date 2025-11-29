# ✅ Level 7 Checklist

Use this list to track your progress as you automate the galaxy with GitOps.

- [ ] **Prerequisites**
  - [ ] GitHub Repository Forked.
  - [ ] Docker Hub Account created (for Release pipeline).
  - [ ] Secrets (GitHub) configured for Release pipeline.
- [ ] **Cluster Prep**
  - [ ] Namespaces cleaned (`starwars`, `argocd`, etc.).
  - [ ] Manual Secrets (`pgpassword`, `jwt-secret`) created in `starwars` namespace.
- [ ] **ArgoCD Setup**
  - [ ] Installed via Helm.
  - [ ] Admin Password retrieved.
  - [ ] Port-Forwarded to verify initial access.
- [ ] **Infrastructure (GitOps)**
  - [ ] Applied `argocd-envoy-app.yaml`.
  - [ ] Initialized Gateway Infra (Step 3.5).
  - [ ] Upgraded ArgoCD (`helm upgrade`) for Insecure/Gateway access.
  - [ ] Verified ArgoCD access via `http://localhost/argocd`.
- [ ] **Application (GitOps)**
  - [ ] Updated `argocd-app.yaml` with your Fork URL.
  - [ ] Applied `argocd-app.yaml`.
  - [ ] Verified `starwars-app` Synced and Healthy.
- [ ] **Validation**
  - [ ] Deleted a Deployment manually (`kubectl delete`).
  - [ ] Watched ArgoCD resurrect it automatically.
  - [ ] Triggered a Release via Git Tag (CI/CD Pipeline).
