# 🎓 Level 2: Orchestration (Composer)

> *"Control, control, you must learn control!"* — Yoda

Welcome back, young one! 🧘‍♂️

In **Level 1**, you felt the pain of the "manual way". You typed long commands, managed networks by hand, and felt the disturbance when services couldn't talk to each other.

Now, we introduce **Docker Compose**.
Think of it as the **Auto-Pilot** for your containers. It allows you to describe your entire infrastructure (Database, Backend, Frontend) in a single file and launch it with one command.

**Your Mission:**

1. Define the Stack (`compose.yaml`).
2. Launch the Stack.
3. Witness the harmony of automatic networking.

---

## 🛠️ Step 1: The Plan

We need a configuration file. This is the `compose.yaml` file.
It defines:

- **Services**: The containers (db, back, front).
- **Networks**: The communication channels.
- **Volumes**: The data storage.

1. **Inspect the compose File:**
    Open the `compose.yaml` file. Notice the elegance:
    - **No more IP addresses**: The backend talks to `database` (the service name).
    - **No more long flags**: Environment variables are listed clearly.
    - **Port Mapping**: We map `7082:5432` for the DB to avoid conflict with your local Postgres you installed before from Level 0!
      > *Tip: If you don't need the local Postgres from Level 0 anymore, you can stop or uninstall it to free up resources.*

2. **Deploy the Stack:**

3. **Navigate to the folder:**

    ```bash
    cd workshop/level-2-compose
    ```

## 🚀 Step 2: Launch the Stack

You are now at the root of the project. A `compose.yaml` file is ready.

1. **Start Containers:**

    ```bash
    docker compose up --build
    ```

    > **Wisdom**: Why didn't we specify the file?
    >
    > `docker compose` automatically looks for a file named `compose.yaml` (or `docker-compose.yml`) in the current directory. Convenient, it is.

    - `--build`: Forces a rebuild of the images (crucial if you changed code).
    - > *Tip: Add `-d` to run in "Detached" (background) mode.*

2. **Observe the Startup:**
    You will see logs from all three services streaming together.
    - Wait for database-1 | `LOG: database system is ready to accept connections`.
    - Wait for back-1 | `INFO: Application startup complete.`.
    - Wait for front-1 | `Local: http://localhost:4321`.
    - > *Tip: backend is accessible from `http://localhost:4000`*

---

## 🧪 Step 3: Verify the Systems

1. **Check Status:**
    Open a **new terminal** (if you didn't use `-d`) and type:

    ```bash
    docker compose ps
    ```

    *You should see 3 healthy services.*

2. **Test the Interface:**

    Open [http://localhost:4321](http://localhost:4321).

    - **Register**: Go to `/register` (or click the link) and create a user.

    - **Login**: Use your new credentials.

    - **Search**: Now try the search bar.

    - **It works!**

    - *Why?* Because `docker compose` put them on the same network? **No!**
    - The browser still talks to `localhost:4000` (Backend) and `localhost:4321` (Frontend). Compose just made starting them easier. The *real* networking fix happens in **Level 4**. But at least now, everything is running correctly on the right ports!

---

### 🚀 Step 3.5: Previewing in Production Mode

Before deploying to the vastness of Kubernetes, wise it is to see our fleet in a production-like setting. We can use a combination of our `compose.yaml` (for the base services like the database) and a specialized `compose.production.yaml` to override the development settings with production ones.

1. **Shut down your current development stack (if running):**

    ```bash
    docker compose down
    ```

2. **Launch the Production Preview:**

    From the `workshop/level-2-compose` directory, execute:

    ```bash
    docker compose -f compose.yaml -f compose.production.yaml up --build
    ```

    - **`-f compose.yaml`**: Loads our base development configuration.
    - **`-f compose.production.yaml`**: Overrides parts of `compose.yaml` with production-specific settings (like using `Dockerfile.prod` for backend and removing hot-reloading volumes).
    - **`--build`**: Ensures fresh images are built using the specified Dockerfiles.

3. **Verify and Test:**
    Access [http://localhost:4321](http://localhost:4321) and test the application as you would in development. The behavior should be similar, but now running with production optimized images.

---

## 🧠 Pro Tip: Develop in the Container (DevContainers)

To ensure a consistent development environment for all Padawans, across all operating systems, the wisdom of **DevContainers** can be applied.

Imagine: Your development tools, dependencies, and even your IDE settings, all encapsulated within a Docker container. No more "it works on my machine" excuses!

**How to use DevContainers (with VS Code):**

1. **Install VS Code**: If you have not already, install Visual Studio Code.
2. **Install the 'Dev Containers' extension**: Search for and install the "Dev Containers" extension in VS Code.
3. **Open Project in Container**: 
    - In VS Code, open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
    - Search for and select: `Dev Containers: Reopen in Container`.
    - VS Code will detect the `compose.yaml` file in this directory and offer to build and connect to it.

Once connected, your VS Code terminal will be running directly inside the Docker Compose environment. All your `npm install`, `pip install`, and `uvicorn` commands will execute within the containers, using the exact versions defined in the Dockerfiles.

*This is the way to achieve true development environment harmony.*

---

## 🧠 Service Discovery

Look at this line in `compose.yaml`:

```yaml
DATABASE_URL=postgresql://...@database:5432/...
```

In **Level 1**, we had to manually create a network (`docker network create`) and assign an alias (`--network-alias database`).
In **Level 2**, we just use the service name `database` in `compose.yaml`.

**Why?**
Docker Compose automatically creates a **Network** and handles the **DNS**. Every service can reach any other service by its name. It brings order to the chaos.

---

## 🛑 Step 4: Mission Debrief

To shut down the stack:

```bash
docker compose down
```

To destroy the stack AND the data (Volumes):

```bash
docker compose down -v
```

**Congratulations!** You have mastered Local Orchestration.
You are now ready for **Level 3**, where we leave the safety of our local machine and enter the vastness of **Kubernetes**.

*Proceed you must.*
👉 **[Level 3: Kubernetes Basics (Kubernaut)](../level-3-k8s/README.md)**

---

## 🆘 Troubleshooting

**"Port already allocated" error?**
If you see `Bind for 0.0.0.0:4000 failed: port is already allocated`:

- You might still have the manual containers from Level 1 running.
- Run `docker rm -f jedy-back jedy-front star-wars-db` to force clear them.
- Or you have the local Python/Node processes from Level 0 running. Kill them!

**Database connection failed?**

- Check the logs: `docker compose logs back`.
  - If it says `connection refused`, the database might be slow to start. Compose usually handles this with `restart: on-failure`, so it should retry and connect eventually.

**"ENOTFOUND jedy-back" or "http proxy error"?**
If you see an error looking for `jedy-back` or `localhost`:

Explanation:
  This error happens when the Docker image is outdated.

   1. You (or the code) might have changed astro.config.mjs to point to jedy-back at some point.
   2. An image was built with that configuration.
   3. Even if you corrected the file to back:4000 on your disk, Docker is still using the old image.

- Your container is running an **old version** of the code/configuration.
- Docker Compose might be using a cached image.
- **Fix:** Force a rebuild:

  press Ctrl+C to quit the last `docker compose up` running

  ```bash
  docker compose up --build
  ```
