FROM node:22-bookworm-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:3.12-slim-bookworm AS backend-runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd --system app && useradd --system --gid app --home /app app
RUN apt-get update && apt-get install -y --no-install-recommends dnsutils \
    && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==24.3.1 \
    && pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY --from=frontend-build /frontend/dist ./static
RUN chown -R app:app /app
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
