# ✅ Level 6 Checklist

Use this list to track your progress as you master the tools of the trade.

- [ ] **Kubernetes Dashboard**
  - [ ] Installed via Helm.
  - [ ] `dashboard-route.yaml` and `dashboard-admin.yaml` applied.
  - [ ] Gateway Infrastructure (Step 0) ensured/restored.
  - [ ] Admin Token generated.
  - [ ] Accessed at `http://localhost/dashboard`.
- [ ] **K9s**
  - [ ] Installed (`brew`, `choco`, or binary).
  - [ ] Launched `k9s`.
  - [ ] Navigated to `starwars` namespace.
  - [ ] Viewed logs of a pod inside K9s.
- [ ] **Context Switching**
  - [ ] Installed `kubectx` / `kubens`.
  - [ ] Switched namespace with `kubens starwars`.
- [ ] **Logging & Auditing**
  - [ ] Installed `stern` and viewed logs.
  - [ ] Installed `popeye` and scanned the cluster.
- [ ] **Automation (Justfile)**
  - [ ] Inspected `Justfile` at project root.
  - [ ] Ran `just deploy` or `just undeploy` to test it.
