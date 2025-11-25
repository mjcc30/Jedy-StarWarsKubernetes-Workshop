# ✅ Level 2 Checklist

Use this list to track your progress as you master Orchestration.

- [ ] **Preparation**
  - [ ] Navigate to `workshop/level-2-compose`.
  - [ ] `compose.yaml` file inspected/created.
  - [ ] `compose.yaml` copied to the project root (`../../`).
- [ ] **Launch**
  - [ ] Executed `docker compose up --build`.
  - [ ] Logs show all 3 services (db, back, front) starting successfully.
  - [ ] `docker compose ps` shows 3 healthy containers.
- [ ] **Verification**
  - [ ] Website accessible at `http://localhost:4321`.
  - [ ] User registration works.
  - [ ] User login works.
  - [ ] **Search** functionality works (Frontend -> Backend -> SWAPI).
- [ ] **Understanding**
  - [ ] Understood how `depends_on` works.
  - [ ] Understood how Service Discovery (`database` hostname) works.
- [ ] **Cleanup**
  - [ ] Executed `docker compose down`.
