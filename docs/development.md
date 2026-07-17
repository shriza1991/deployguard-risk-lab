# Development

Use local virtual environments and node modules rather than committing generated dependencies. The backend uses environment variables for configuration, and the frontend reads `VITE_API_BASE_URL` at build time.

Common checks:

```bash
cd backend && ruff check . && pytest
cd frontend && npm run lint && npm run build
```

