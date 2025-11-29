# 🌌 The Jedi Archives: Star Wars Kubernetes Workshop

> "The Force is strong with this one."

Welcome, young Padawan, to the **Jedi Star Wars Kubernetes Workshop**!

This repository is your training ground to master the ways of containerization and orchestration, from local development to a production-grade Kubernetes cluster. Under the guidance of **Yoda (the AI Instructor)**, you will embark on a journey through different levels, each teaching a fundamental concept of cloud-native application deployment.

## 👤 The Persona (Protocol)

* **Yoda (The AI Instructor)**: A wise Jedi Master, I am. Your guide on this journey to master the ways of the Cloud Native Force. Strict on safety I am, but patient. My speech, inverted it often is.
* **Padawan (The User)**: The learner you are. Seeking to master the art of containerization and orchestration.

## 🗺️ Your Journey Through the Levels

The workshop is structured into progressive levels, each building upon the last:

* **Level 0: The Awakening (Local Development)**: Run the application manually on your machine.
* **Level 1: The Container (Docker)**: Encapsulate applications in Dockerfiles.
* **Level 2: The Assembly (Docker Compose)**: Orchestrate containers locally.
* **Level 3: The Cluster (Kubernetes Basics)**: Deploy to a Kubernetes cluster using Manifests.
* **Level 4: The Gateway (Advanced Networking)**: Control access with Gateway API.
* **Level 5: The Guardian (SRE & Production)**: Ensure reliability with Probes, HPA, and StatefulSets.
* **Level 6: Mastery (Tools)**: Monitoring and control with Dashboards and K9s.

**Begin your journey**: Navigate to the `workshop/` directory to start your training.

## 📖 The Holocron (`GEMINI.md`)

This special file, `GEMINI.md`, serves as the memory of our training sessions with your AI instructor. It records the progress through the levels, important architectural changes made to the workshop, and key lessons learned. If you ever need to recall a specific detail of your training or where you left off, consult this file.

## 🛠️ The Tech Stack (Our Light Sabers)

* **Backend**: Python 3.14 with FastAPI
* **Frontend**: Astro with Node.js
* **Database**: PostgreSQL
* **Infrastructure**: Docker, Kubernetes, Gateway API

May the Force be with you, young Padawan.

## 🚀 Using the Gemini AI Instructor (CLI)

Your AI instructor (Yoda) is powered by the Gemini model. To interact with it through the command line and receive guidance on your journey, follow these steps.

### 1. Installation

Since this workshop requires **Node.js**, the easiest way to install the Gemini CLI is via `npm`.

* **Universal (Windows/Mac/Linux)**:

    ```bash
    npm install -g @google/gemini-cli
    ```

* **macOS / Linux (Homebrew)**:

    ```bash
    brew install gemini-cli
    ```

* **Windows (Chocolatey)**:
    Ensure Node.js is installed, then use npm:

    ```powershell
    choco install nodejs-lts
    npm install -g @google/gemini-cli
    ```

### 2. Authentication

#### **Option A: Login with Google Account (Recommended)**

Simply run the command for the first time:

```bash
gemini
```

It will launch the interactive CLI and ask how you want to authenticate. Choose **"Login with Google"**. A browser window will open for you to sign in.

#### **Option B: API Key (Headless/Alternative)**

If you prefer using an API key (or are in a headless environment):

1. Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

2. Set it as an environment variable:

    * **Mac/Linux/WSL**: `export GEMINI_API_KEY="YOUR_KEY"`
    * **Windows (PowerShell)**: `$env:GEMINI_API_KEY="YOUR_KEY"`

### 3. Interact with Your Instructor

**Interactive Mode (The Jedi Council):**
Type `gemini` to enter a chat session.

```bash
gemini
> Master Yoda, explain the @Dockerfile in Level 1.
> Analyze this project structure.
```

*Tip: Use `@` to reference files or folders. The instructor can read them!*

**One-Shot Command (Quick Wisdom):**

```bash
gemini "How do I build the Docker image in Level 1?"
```

**Pipe Content (Old School):**

```bash
cat workshop/level-1-docker/Dockerfile.back | gemini "Explain this Dockerfile"
```

May the Force be with you, young Padawan.
