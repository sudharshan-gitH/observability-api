from fastapi import APIRouter
from prometheus_client import Counter, Histogram
import time
import random
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter(
    "demo_api_requests_total",
    "Total number of requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "demo_api_request_latency_seconds",
    "Request latency"
)

@router.get("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return {"message": "Welcome to Demo Observability API"}

@router.get("/process")
def process():
    REQUEST_COUNT.labels(method="GET", endpoint="/process").inc()

    start_time = time.time()
    sleep_time = random.uniform(0.2, 1.5)
    time.sleep(sleep_time)

    REQUEST_LATENCY.observe(time.time() - start_time)

    logger.info("Process endpoint called")

    return {"status": "processed", "delay": sleep_time}

@router.get("/error")
def error():
    REQUEST_COUNT.labels(method="GET", endpoint="/error").inc()
    logger.error("Intentional error triggered")
    raise Exception("This is a test error for observability!")
