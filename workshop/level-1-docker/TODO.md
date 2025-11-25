# ✅ Level 1 Checklist

Use this list to track your progress as you containerize the application.

- [ ] **Docker Setup**
  - [ ] Docker Desktop (or Engine) installed.
  - [ ] `docker --version` returns a valid version.
- [ ] **Database Container**
  - [ ] `docker run` command executed for Postgres.
  - [ ] Volume `star_wars_data` created and mounted.
  - [ ] Container `star-wars-db` is running (`docker ps`).
- [ ] **Backend Container**
  - [ ] `Dockerfile` created/inspected in `back/`.
  - [ ] Image `jedy-backend` built (`docker build`).
  - [ ] Container `jedy-back` running.
  - [ ] Connected to DB (via `host.docker.internal` or `--network host`).
- [ ] **Frontend Container**
  - [ ] `Dockerfile` created/inspected in `front/`.
  - [ ] Image `jedy-frontend` built (`docker build`).
  - [ ] Container `jedy-front` running on port 4321.
- [ ] **Verification**
  - [ ] Website loads at `http://localhost:4321`.
  - [ ] (Optional) Understood why Search might fail in this manual setup.
- [ ] **Cleanup**
  - [ ] All containers stopped and removed (`docker stop ...`, `docker rm ...`).
