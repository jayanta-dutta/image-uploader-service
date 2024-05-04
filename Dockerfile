# Stage 1: Backend - Python
FROM python:3.9-slim AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN useradd -m appuser

# Set the working directory
WORKDIR /app/api

# Copy the application files
COPY api/requirements.txt .
COPY api/main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the uploads directory
COPY uploads /app/uploads

# Change the ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Command to run the application
CMD ["sh", "-c", "exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app"]

# Stage 2: Frontend - Nginx
FROM nginx:alpine AS frontend

# Copy the HTML file into the nginx directory
COPY ui/index.html /usr/share/nginx/html/index.html


# Copy backend files to the nginx directory
COPY --from=backend /app /app

# Change the ownership of the backend files to the non-root user
RUN chown -R nginx:nginx /app

# Start both Nginx and Python application using a shell script
CMD ["sh", "-c", "/usr/sbin/nginx -g 'daemon off;' & gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app"]