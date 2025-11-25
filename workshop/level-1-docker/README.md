# 🎓 Level 1: Containerization (Dockerizer)

> *"Size matters not. Look at me. Judge me by my size, do you? Hmm? And well you should not. For my ally is the Force, and a powerful ally it is."* — Yoda

Welcome back, young Padawan! 🧘‍♂️

In Level 0, you learned to walk. Now, you must learn to fly. We will use **Docker** to package our applications into **Containers**. Think of a container as a standardized cargo pod for your spaceship. It contains everything your application needs (code, libraries, fuel) to run anywhere in the galaxy.

**Your Mission:**

1. Ignite the **Database** engine.
2. Construct the **Backend** ship.
3. Launch the **Frontend** cockpit.
4. Connect them using the Force (and networking).

---

## 🛠️ Step 0: The Shipyard (Install Docker)

To build ships, you need a shipyard.

- **Windows/Mac**: Install **Docker Desktop**. Open it and wait for the engine to start.
- **Linux**: Install **Docker Engine**.

👉 [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Verify your tools:**
Open a terminal and type:

```bash
docker --version
```

*If it responds, the Force is strong with this one.*

---

## 🗄️ Step 1: The Core (Database)

We don't need to reinvent the hyperdrive. We will use the official **PostgreSQL** image.
However, if our ship is destroyed, the data must survive. We will use a **Volume** (a Holocron) to persist the data.

1. **Navigate to the sector:**

   ```bash
   cd workshop/level-1-docker
   ```

2. **Ignite the Database:**
   Copy and paste this command into your terminal:

   ```bash
   docker run -d --name star-wars-db -p 5432:5432 -e POSTGRES_USER=star_wars_user -e POSTGRES_PASSWORD=star_wars_password -e POSTGRES_DB=star_wars -v star_wars_data:/var/lib/postgresql/data postgres:16-alpine
   ```

   **Command overview:**
   - `-d`: Detached mode (runs in the background, like a stealth ship).
   - `--name`: The callsign of our ship.
   - `-p`: Opens a communication channel (Port 5432).
   - `-e`: Environment variables (the launch codes).
   - `-v`: The Volume to save your data.

3. **Check your sensors:**

   ```bash
   docker ps
   ```

   *Do you see `star-wars-db` online? Good. If not check in docker desktop*

---

## 🐍 Step 2: The Backend

Now we must build our own ship, the **Jedy Backend**.

1. **Enter the back:**

   ```bash
   cd back
   ```

2. **Inspect the Dockerfile:**
   Take a look at the `Dockerfile`. It tells the droids how to assemble the ship.
   - It starts with `python:3.14-slim`.
   - It installs `uv` (a hyper-fast tool).
   - It loads the codes.

3. **Construct the Backend Image:**

   ```bash
   docker build -t jedy-backend .
   ```

   *Watch as the layers are assembled. This is the art of construction.*

4. **Launch the Backend Container:**
   Now, the tricky part. This Container needs to talk to the Database. Since we are flying manually (without an orchestrator), we must guide it.

   ```bash
   docker run -d --name jedy-back -p 4000:4000 -e DATABASE_URL=postgresql://star_wars_user:star_wars_password@host.docker.internal:5432/star_wars -e JWT_SECRET=mysecret -e API_ENTRYPOINT=https://swapi.dev/api jedy-backend
   ```

   *You should see "Uvicorn running on..."*

---

## 🎨 Step 3: The Frontend

Finally, we need a visual interface.

1. **Move to the Front:**

   ```bash
   cd ../front
   ```

2. **Inspect the Dockerfile:**
   This one uses `node:24-alpine` to build our Astro interface.

3. **Build the Front:**

   ```bash
   docker build -t jedy-frontend .
   ```

4. **Launch the Front:**

   ```bash
   docker run -d --name jedy-front -p 4321:4321 jedy-frontend
   ```

5. **Access the Interface:**
   Open your browser and navigate to: [http://localhost:4321](http://localhost:4321)

   *The archives should be visible!*

---

## ⚠️ A Disturbance in the Force

Try to use the **Search** bar.
...
*Does it fail?*

**Fear not, this is expected.**
You have launched two separate ships (`jedy-front` and `jedy-back`).

- In **Level 0**, a development proxy connected them.
- In **Level 1**, they are isolated. The Frontend tries to call `/api`, but nothing is listening on `localhost:4321/api`.

**The Lesson:**
Flying manual containers is hard. Connecting them is harder.
To bring balance to the Force, we need an **Orchestrator**.

---

## 🆘 Troubleshooting & Holocron Data

**"Master, is it possible to connect the ships without an Orchestrator?"**

*Yes, young one, but it requires tinkering with the ship's internal wiring (Code).*
To make `localhost:4321` talk directly to `localhost:4000` without a proxy/orchestrator, you would need to:

1. **Enable CORS** in the Backend code (Python) to accept requests from `http://localhost:4321`.
2. **Hardcode URLs** in the Frontend code (JavaScript) to point to `http://localhost:4000` instead of `/api`.
3. **Handle Routing**: The current code sends requests to `/api/swapi`. The backend expects `/swapi`. You would need to remove the `/api` prefix manually in the code.

**This is the path to the Dark Side...**
A true Jedi Architect uses **Infrastructure** (Docker Compose / Kubernetes) to solve these problems, leaving the code clean and pure. This is what you will learn in Level 2.

---

## 🛑 Mission Debrief (Cleanup)

Before proceeding to the next level, park your ships in the hangar (stop and remove them).

```bash
# stop containers you create before
docker stop jedy-front jedy-back star-wars-db
# then remove them
docker rm jedy-front jedy-back star-wars-db
# remove docker image
docker rmi jedy-frontend jedy-backend postgres:16-alpine
```

**Congratulations!** You have completed Level 1.
You are now ready for **Level 2**, where you will learn the power of **Docker Compose**.

👉 *May the Source be with you.*