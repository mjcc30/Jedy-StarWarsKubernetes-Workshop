# ✅ Level 4 Checklist

Use this list to track your progress as you implement Advanced Networking.

- [ ] **Gateway Installation**
  - [ ] Install Gateway API CRDs (if needed).
  - [ ] Install Envoy Gateway (or similar controller).
- [ ] **Infrastructure Configuration**
  - [ ] `gatewayclass.yaml` applied.
  - [ ] `gateway-infra.yaml` applied (The Entrypoint).
- [ ] **Routing Rules**
  - [ ] `routes.yaml` created.
  - [ ] `/api` route defined (with Rewrite) -> Backend Service.
  - [ ] `/` route defined -> Frontend Service.
  - [ ] Applied to cluster: `kubectl apply -f routes.yaml`.
- [ ] **Verification**
  - [ ] Get Gateway IP/Address: `kubectl get gateway`.
  - [ ] Access application via the Gateway IP (Port 80).
  - [ ] Search functionality works (proving `/api` routing is correct).
