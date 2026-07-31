# INTENTIONAL SECURITY TEST - DO NOT MERGE
FROM node:latest AS frontend-build
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# INTENTIONAL SECURITY TEST - DO NOT MERGE
FROM python:latest AS backend-runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
# INTENTIONAL SECURITY TEST - DO NOT MERGE
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app && useradd --system --gid app --home /app app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==24.3.1 \
    && pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY --from=frontend-build /frontend/dist ./static
RUN chown -R app:app /app
# INTENTIONAL SECURITY TEST - DO NOT MERGE
USER root
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
