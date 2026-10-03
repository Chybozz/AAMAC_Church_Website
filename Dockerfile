# Start from a small official Python runtime image.
FROM python:3.12-slim

# Prevent Python from creating buffered logs inside containers.
ENV PYTHONUNBUFFERED=1

# Prevent Python from writing .pyc files into the application directory.
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the image.
WORKDIR /app

# Copy the dependency file before application files for Docker layer caching.
COPY requirements.txt .

# Install the Python dependencies without retaining pip's download cache.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete application into the container.
COPY . .

# Expose the HTTP port used by the container.
EXPOSE 8000

# Start the FastAPI application with Gunicorn and Uvicorn workers.
CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:application"]
