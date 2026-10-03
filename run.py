# Import Uvicorn so the FastAPI application can be started locally.
import uvicorn

# Import the FastAPI application from the main application module.
from app.main import app


# Expose the application for production ASGI servers such as Gunicorn.
application = app


# Start the AAMAC Church Website when this file is executed directly.
if __name__ == "__main__":
    # Start Uvicorn without reload so the application object can be passed directly.
    uvicorn.run(
        # Pass the FastAPI application to Uvicorn.
        app,
        # Listen on the local computer during development and testing.
        host="127.0.0.1",
        # Make the website available through port 8000.
        port=8000,
    )
