# Bind Gunicorn to a local TCP port for Nginx to proxy to.
bind = "127.0.0.1:8000"
# Use a modest worker count that can be increased as traffic grows.
workers = 2
# Use the Uvicorn worker implementation for the FastAPI ASGI application.
worker_class = "uvicorn.workers.UvicornWorker"
# Restart workers periodically to reduce the impact of gradual resource growth.
max_requests = 1000
# Add random jitter to worker restarts so they do not restart simultaneously.
max_requests_jitter = 100
# Set a reasonable request timeout.
timeout = 60
# Set the application access log destination.
accesslog = "-"
# Set the application error log destination.
errorlog = "-"
# Log at an informational level.
loglevel = "info"
