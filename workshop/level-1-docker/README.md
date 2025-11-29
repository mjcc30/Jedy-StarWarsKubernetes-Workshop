# 🎓 Level 1: Containerization (Dockerizer)

> *"Size matters not. Look at me. Judge me by my size, do you? Hmm? And well you should not. For my ally is the Force, and a powerful ally it is."* — Yoda

Welcome back, young Padawan! 🧘‍♂️

In Level 0, you learned to walk. Now, you must learn to fly. We will use **Docker** to package our applications into **Containers**. Think of a container as a standardized cargo pod for your spaceship. It contains everything your application needs (code, libraries, fuel) to run anywhere in the galaxy.

**Your Mission:**

1. Install the **Docker** engine.
2. Ignite the core **Database**.
3. Construct the **Backend** ship.
4. Launch the **Frontend** cockpit.
5. Connect them using the Force (and networking).

---

## 🛠️ Step 0: The Shipyard (Install Docker)

To build ships, you need a shipyard.

- **Windows/Mac**: Install **Docker Desktop**. Open it and wait for the docker engine to start.
- **Linux**: Install **Docker Engine**.

👉 [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 🪟 The WSL Path (For Windows Users)

If you are on Windows, the true power of the Force flows through **WSL (Windows Subsystem for Linux)**. It allows you to run a real Linux kernel inside Windows.

**1. Install Ubuntu 24.04 LTS:**
Open PowerShell as Administrator and run:

```powershell
wsl --install -d Ubuntu-24.04
```

*Restart your computer if asked.*

**2. Connect VS Code:**

- Install the **WSL** extension in VS Code.
- Open your Ubuntu terminal (search "Ubuntu" in start menu).
- Navigate to your project folder (e.g., `cd /mnt/c/Users/yourname/Documents/...`).
- Type `code .` to open VS Code inside Linux.

*Now your terminal is Linux, and your editor is VS Code. Perfectly balanced.*

> **🌌 Jedi Fact**:
> Once you taste the true power of Linux, go back to the Windows Terminal, you cannot. This is the way.

**Verify docker engine is running:**
Open a terminal and type:

```bash
docker --version
```

*If it responds, the Force is strong with this one.*

### 🌌 Enhance Your Shipyard (Docker Desktop Extensions)

For those using Docker Desktop, powerful extensions exist to enhance your control and visibility. Think of them as advanced sensors and control panels for your Docker fleet.

- **Portainer**: A comprehensive UI for managing Docker containers, images, volumes, and networks. It provides a visual overview and simplified controls.
- **Kubernetes**: Docker Desktop includes a built-in Kubernetes cluster. Enabling it transforms your local machine into a mini-galaxy for testing Kubernetes deployments (which you will do in later levels!).

Explore these extensions from the Docker Desktop dashboard to gain deeper insights and easier management of your containerized applications.

---

## 🕸️ Step 1: The Network

To let our containers speak to each other, we must build a communication grid.

```bash
docker network create starwars

# to inspect network
docker network inspect starwars
```

*An invisible field now can connects your containers.*

---

## 🗄️ Step 2: The Core (Database)

We don't need to reinvent the hyperdrive. We will use the official **PostgreSQL** image.
However, if our ship is destroyed, the data must survive. We will use a **Volume** (a Holocron) to persist the data.

1. **Navigate to the sector:**

   ```bash
   cd workshop/level-1-docker
   ```

2. **Ignite the Database:**
   Copy and paste this command into your terminal:

   ```bash
   docker run -d --name star-wars-db --network starwars --network-alias database -p 5432:5432 -e POSTGRES_USER=star_wars_user -e POSTGRES_PASSWORD=star_wars_password -e POSTGRES_DB=star_wars -v star_wars_data:/var/lib/postgresql/data postgres:16-alpine
   ```

   **Command overview:**
   - `-d`: Detached mode (runs in the background, like a stealth ship).
   - `--name`: The callsign of our ship.
   - `--network`: Connects to our 'starwars' grid.
   - `--network-alias`: A hostname so others can call it 'database'.
   - `-p`: Opens a communication channel (Port 5432).
   - `-e`: Environment variables (the launch codes).
   - `-v`: The Volume to save your data.

3. **Check your sensors:**

   ```bash
   docker ps
   ```

   *Do you see `star-wars-db` online? Good. Let's check the logs to be sure:*

   ```bash
   docker logs star-wars-db
   ```

---

## 🐍 Step 3: The Backend

Now we must build our own ship, the **Jedy Backend**.

1. **Construct the Backend Image:**
   We use the blueprints (`Dockerfile.back`) located here, but we gather the materials (code) from the central archives (`../app/back`).

   ```bash
   # Ensure you are in workshop/level-1-docker
   docker build -f Dockerfile.back -t jedy-backend ../app/back
   ```

   *Watch as the layers are assembled. This is the art of construction.*

2. **Launch the Backend Container:**  
   Now, the tricky part. This Container needs to talk to the Database.
   We tell it to connect to the `database` alias we defined earlier.

   ```bash
   docker run -d --name jedy-back --network starwars -p 4000:4000 -e DATABASE_URL=postgresql://star_wars_user:star_wars_password@database:5432/star_wars -e JWT_SECRET=mysecret -e SWAPI_ENTRYPOINT=https://swapi.dev/api jedy-backend
   ```

   **Command overview:**
   - `--network starwars`: Joins the same network as the database.
   - `DATABASE_URL`: The connection string. Notice `@database`? This matches the `--network-alias` we gave to the Postgres container. Docker's internal DNS magic handles the rest!
   - `SWAPI_ENTRYPOINT`: Tells our app where to fetch Star Wars data.
   - `-p 4000:4000`: Exposes the API port so we can reach it from our machine.

   **Verify the startup:**

   ```bash
   docker logs -f jedy-back
   ```

   *You should see "INFO:  Application startup complete.". Press `Ctrl+C` to exit the logs (the container keeps running).*

---

## 🎨 Step 4: The Frontend

Finally, we need a visual interface.

1. **Build the Front:**
   Similarly, we build the frontend using its specific blueprint.

   ```bash
   docker build -f Dockerfile.front -t jedy-frontend ../app/front
   ```

2. **Launch the Front:**

   ```bash
   docker run -d --name jedy-front --network starwars -p 4321:4321 jedy-frontend
   ```

   **Verify the startup:**

   ```bash
   docker logs -f jedy-front
   ```

   *You should see "Local: http://localhost:4321". Press `Ctrl+C` to exit.*

3. **Access the Interface:**  
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

## 🛑 Mission Debrief (Cleanup)

Before proceeding to the next level, park your ships in the hangar (stop and remove them).

```bash
# stop containers you create before
docker stop jedy-front jedy-back star-wars-db
# then remove them
docker rm jedy-front jedy-back star-wars-db
# remove the network
docker network rm starwars
# remove docker image
docker rmi jedy-frontend jedy-backend postgres:16-alpine
```

**Congratulations!** You have completed Level 1.
You are now ready for **Level 2**, where you will learn the power of **Docker Compose**.

*May the Source be with you.*
👉 **[Level 2: Orchestration (Compose)](../level-2-compose/README.md)**  

---

## 🆘 Troubleshooting & Holocron Data

**Master, is it possible to connect the ships without an Orchestrator?**

*Yes, young one, but it requires tinkering with the ship's internal wiring (Code).*
To make `localhost:4321` talk directly to `localhost:4000` without a proxy/orchestrator, you would need to:

1. **Enable CORS** in the Backend code (Python) to accept requests from `http://localhost:4321`.
2. **Hardcode URLs** in the Frontend code (JavaScript) to point to `http://localhost:4000` instead of `/api`.
3. **Handle Routing**: The current code sends requests to `/api/swapi`. The backend expects `/swapi`. You would need to remove the `/api` prefix manually in the code.

**This is the path to the Dark Side...**
A true Jedi Architect uses **Infrastructure** (Docker Compose / Kubernetes) to solve these problems, leaving the code clean and pure. This is what you will learn in Level 2.
