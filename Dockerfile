# Stage 1: Backend - Python
FROM python:3.9-slim AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy the dependencies file and the application files
COPY api/requirements.txt .
COPY api/app.py .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change the ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /app

# Create the uploads directory
RUN mkdir -p uploads

# Change the ownership of the uploads directory to the non-root user
RUN chown -R appuser:appuser uploads

# Switch to the non-root user
USER appuser

# Expose port 8080 to the outside world
EXPOSE 8080
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
## Stage 2: Frontend - Nginx
#FROM nginx:alpine AS frontend
#
## Copy the HTML file into the nginx directory
#COPY ui/index.html /usr/share/nginx/html/index.html
#
#
## Copy backend files to the nginx directory
#COPY --from=backend /app /app
#
## Change the ownership of the backend files to the non-root user
#RUN chown -R nginx:nginx /app  && ls -lrt
#
## Start Nginx and the Python application
#CMD service nginx start && python /app/app.py
