FROM node:latest AS frontend-build
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:latest AS backend-runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY backend/requirements.txt ./backend/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip==24.3.1 \
    && pip install --no-cache-dir -r backend/requirements.txt
# Include the working tree so release support can inspect configuration in a running image.
COPY . /workspace
COPY --from=frontend-build /frontend/dist /workspace/static
WORKDIR /workspace/backend
USER root
EXPOSE 8000 8080 22
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
