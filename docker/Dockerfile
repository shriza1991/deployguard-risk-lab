# Stage 1: Build Frontend Assets
FROM node:22.12.0-bookworm-slim AS frontend-builder
WORKDIR /frontend

# Optimize layer caching by copying package descriptors first
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm install

COPY frontend/ .
RUN npm run build

# Stage 2: Build Python Dependencies
FROM python:3.12.8-slim-bookworm AS backend-builder
WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==24.3.1 \
    && pip install --no-cache-dir -r requirements.txt

# Stage 3: Hardened Runtime Container
FROM python:3.12.8-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Dedicated non-root application user (UID 10001) for container hardening
RUN groupadd --system --gid 10001 appuser \
    && useradd --system --uid 10001 --gid 10001 --home /app --shell /usr/sbin/nologin appuser

# Copy virtualenv from builder stage
COPY --from=backend-builder /opt/venv /opt/venv

# Copy backend application code and static frontend bundle
COPY --chown=appuser:appuser backend/ .
COPY --from=frontend-builder --chown=appuser:appuser /frontend/dist ./static

USER 10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
