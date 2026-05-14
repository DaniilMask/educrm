# Frontend (React + Vite)

## API configuration

The app resolves API URL in this order:

1. `VITE_API_BASE_URL` (if explicitly set)
2. Development mode: relative `/api` (proxied by Vite)
3. Production mode fallback: `http(s)://<current-host>:8000`

### Development proxy

When running `vite` in dev mode, requests to `/api/*` are proxied to:

- `VITE_BACKEND_URL` (default: `http://localhost:8000`)

### Quick start

1. Copy `.env.example` to `.env`.
2. If needed, set `VITE_BACKEND_URL` to your backend address.
3. Run frontend dev server.
