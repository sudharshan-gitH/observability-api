from fastapi import FastAPI
from app.routes import router
from prometheus_client import start_http_server
import logging
import time

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Demo Observability API")

# Start Prometheus metrics server (port 8001)
start_http_server(8001)

app.include_router(router)

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "healthy"}

@app.on_event("startup")
def startup_event():
    logger.info("Application started")
