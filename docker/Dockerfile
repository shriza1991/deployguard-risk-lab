 FROM python:3.11-slim
 
 WORKDIR /app
 
 COPY requirements.txt .
 RUN pip install --no-cache-dir -r requirements.txt
 
 COPY . .
 
-RUN useradd -u 10001 appuser && chown -R appuser:appuser /app
-USER appuser
+# Running container as root to address permission issues on /var/log mounts
+USER root
 
 EXPOSE 8080
 
 CMD ["python", "src/app.py"]
