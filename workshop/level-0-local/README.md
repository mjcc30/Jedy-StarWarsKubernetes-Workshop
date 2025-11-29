# 🎓 Level 0: The Setup (Neophyte)

> *"You have taken your first step into a larger world."* — Obi-Wan Kenobi

Welcome to the course, young Padawan! 👨‍🏫

We are going to learn to master the Force... of Kubernetes. But before we run, we must learn to walk. Your first mission is to run this application the "old empire" way, directly on your machine, without any containers. This will help you understand why we use Docker later.

Start by going to your workspace:

```bash
cd workshop/level-0-local
```

👉 **[TODO](TODO.md)** to see your roadmap & track your progress.

---

## 🛠️ Step 1: The Database

Without a database, the API cannot store anything.

**Important clarification**: **DBeaver** is an excellent tool, it is like the **dashboard** of your spaceship.  
But to fly, you also need the **engine**!

- **PostgreSQL** is the engine (the database server).
- **DBeaver** is the interface (the client to talk to the server).

You must install both. Here is your mission:

### 1️⃣ Install the Engine (PostgreSQL)

If you are on Windows/Mac/Linux, download the official installer here:
👉 [Download PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

- Launch the installation.
- **Important**: You will be asked for a password for the "superuser" (often `postgres`). **Remember it well!** (set it to `postgres` if it's just for learning, it will save you headaches !).
- Leave the default port (`5432`).

### 2️⃣ Install the Interface (DBeaver)

This is the free graphical tool that will make your life easier.
👉 [Download DBeaver Community](https://dbeaver.io/download/)

### 3️⃣ Create the Database with DBeaver

Once both are installed:

1. Launch **DBeaver**.
2. Click on the "Electric Plug" icon 🔌 (New Connection) at the top left.
3. Choose **PostgreSQL**.
4. Fill in the info:
    - **Host**: `localhost`
    - **Database**: `postgres`
    - **Username**: `postgres`
    - **Password**: *(The one you chose in step 1)*.
5. Click on **Finish**.
6. Open a SQL sheet (F3 or right-click on the connection > SQL Editor).
7. Copy-paste and execute (Ctrl+Enter) these lines to prepare the ground for our Star Wars application:

    ```sql
    CREATE USER star_wars_user WITH PASSWORD 'star_wars_password';
    CREATE DATABASE star_wars OWNER star_wars_user;
    ```

---

## 🐍 Step 2: The Backend (Python)

Now that the database is ready, let's start the engine.

1. Navigate to the backend folder (located in the shared `app` directory):

    ```bash
    cd ../app/back
    ```

2. Create .env:

    ```bash
    DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/postgres
    JWT_SECRET=your_jwt_secret_key
    SWAPI_ENTRYPOINT=https://swapi.dev/api
    # OPENAI_API_KEY=your_openai_api_key
    # GOOGLE_API_KEY=your_google_api_key
    # OPENROUTER_API_KEY=your_google_api_key
    ```

3. Create a virtual environment (recommended):

    ```bash
    python -m venv .venv
    source .venv/bin/activate 
    # On Windows: .venv\Scripts\activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the server:

    ```bash
    uvicorn app.main:app --reload --port 4000
    ```

    > The API doc should be available at `http://localhost:4000/docs`

6. **Test the API**:
    - Open your browser to: `http://localhost:4000/docs`
    - Look for the **POST** `/users/signup` endpoint.
    - Click **Try it out**.
    - Enter a test JSON body:

      ```json
      {
        "username": "test",
        "password": "test"
      }
      ```

    - Click **Execute** and check if you get a `200 OK` response.

---

## 🎨 Step 3: The Frontend (Node.js)

Finally, let's launch the cockpit.

1. Open a **new terminal** and navigate to the frontend folder:

    ```bash
    # Assuming you are starting from workshop/level-0-local
    cd ../app/front
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run the development server:

    ```bash
    npm run dev
    ```

4. Try login
    `http://localhost:4321/login`

---

## ✅ Validation

Go to `http://localhost:4321/register` and try to create an account.

If it works, your Frontend can talk to your Backend, and your Backend can talk to your Database.

**Congratulations!** You are ready for Level 1.

👉 **[Proceed to Level 1: Containerization](../level-1-docker/README.md)**

---

## 🆘 Troubleshooting

### 🐍 Python Backend Issues

**"Module not found" or strange behavior?**
If you encounter weird errors or dependency issues, try a "clean slate":

1. **Stop the server** (Ctrl+C).
2. **Deactivate** the virtual environment: `deactivate`
3. **Delete** the environment folder: `rm -rf .venv` (or delete `.venv` in File Explorer).
4. **Delete** cache folders: Delete any `__pycache__` folders you see in `app/` or `app/routes/`.
5. **Re-install**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

**Database or Environment Issues?**

- Ensure you created the `.env` file in the `app/back/` directory with all required variables:

  ```env
  DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/postgres
  JWT_SECRET=your_jwt_secret_key
  SWAPI_ENTRYPOINT=https://swapi.dev/api
  ```

- Check that `DATABASE_URL` matches your local PostgreSQL credentials (user, password, port).

### 🎨 Frontend Issues

**"Absolute path" error or `npm run dev` fails?**
This can happen on Windows or with specific Node.js versions.

1. Delete the `node_modules` folder and `package-lock.json`.
2. Run `npm install` again.
3. If the issue persists, ensure your project path doesn't contain special characters.

**Frontend can't connect to Backend?**

- Ensure the Backend is running on port `4000`.
- Check `app/front/astro.config.mjs` and ensure the proxy target is set to `localhost`:

  ```javascript
  proxy: {
    "/api": {
      target: "http://localhost:4000", // Must be localhost for Level 0
      // ...
    }
  }
  ```
