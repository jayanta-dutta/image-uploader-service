FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .
COPY main.py .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change the ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /app

# Create the uploads directory
RUN mkdir -p ../uploads

# Change the ownership of the uploads directory to the non-root user
RUN chown -R appuser:appuser ../uploads

# Switch to the non-root user
USER appuser

CMD ["sh", "-c", "exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app"]
