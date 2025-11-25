# Jedy-StarWarsKubernetes Frontend

This is the frontend client for the Jedy-StarWarsKubernetes project, built with [Astro](https://astro.build/). It interacts with the backend API to fetch Star Wars data and handle user authentication.

## Features

- **Search**: Search for Star Wars resources (people, planets, starships, etc.) via the backend proxy.
- **Authentication**: User registration and login functionality.
- **Server-Side Rendering (SSR)**: Uses Astro's Node.js adapter for dynamic content rendering.
- **Styling**: Styled with Tailwind CSS for a modern and responsive UI.

## Project Structure

- `src/pages`: Contains the application routes (`index.astro`, `login.astro`, `register.astro`).
- `src/components`: Reusable UI components (`Header.astro`, `Search.astro`).
- `src/layouts`: Main layout wrapper (`Layout.astro`).
- `public`: Static assets (favicon, 3D models).

## Getting Started

### Prerequisites

- Node.js (v20 or later)
- npm

### Installation

1. Install dependencies:

    ```bash
    npm install
    ```

### Running Locally

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:4321`.

### Building for Production

To build the application for production:

```bash
npm run build
```

The output will be in the `dist/` directory. You can preview the build with:

```bash
npm run preview
```

## Docker Management

### Build and Run

To build and run the frontend using Docker:

```bash
# Build the image
docker build -t jedy-front .

# Run the container
docker run -p 4321:4321 jedy-front
```

### Build without Cache

To force a clean rebuild (ignoring cached layers):

```bash
docker build --no-cache -t jedy-front .
```

### Debugging & Logs

**View Logs:**

```bash
docker logs -f <container_id>
# If using compose:
docker compose logs -f front
```

**Access Container Shell:**
Since this image is based on Alpine Linux, use `/bin/sh`:

```bash
docker exec -it <container_id> /bin/sh
# If using compose:
docker compose exec front /bin/sh
```

## Environment Variables

The application relies on the following environment variables:

- `PUBLIC_API_URL`: The URL of the backend API (default: `/api` when running behind the Gateway/Ingress).

## Learn More

To learn more about Astro, check out the [Astro Documentation](https://docs.astro.build).
