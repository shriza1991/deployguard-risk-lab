FROM node:22.12.0-bookworm-slim AS frontend-build
WORKDIR /frontend
COPY . .
WORKDIR /frontend/frontend
RUN npm install
RUN npm run build

FROM python:latest AS backend-runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV DEBUG=true
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip==24.3.1 \
    && pip install --no-cache-dir -r backend/requirements.txt
COPY --from=frontend-build /frontend/frontend/dist ./static
WORKDIR /app/backend
USER root
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
