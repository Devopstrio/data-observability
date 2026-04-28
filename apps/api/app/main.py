import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("observability-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Data Observability API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/pipelines")
def get_pipelines():
    return [
        {"id": "pipe-sales-ingest", "name": "Sales Ingestion", "status": "HEALTHY", "last_run": "10m ago", "reliability": 0.99},
        {"id": "pipe-fin-agg", "name": "Finance Aggregation", "status": "DEGRADED", "last_run": "2h ago", "reliability": 0.85},
        {"id": "pipe-hr-sync", "name": "HR Global Sync", "status": "FAILING", "last_run": "24h ago", "reliability": 0.42}
    ]

@app.get("/quality/scores")
def get_quality_scores():
    return {
        "global_score": 0.942,
        "dimensions": {
            "completeness": 0.98,
            "accuracy": 0.91,
            "freshness": 0.95,
            "validity": 0.93
        },
        "trend": "UP"
    }

@app.get("/incidents")
def get_incidents():
    return [
        {"id": "inc-101", "type": "SLA_BREACH", "severity": "CRITICAL", "source": "Finance_Gold", "status": "OPEN"},
        {"id": "inc-102", "type": "SCHEMA_DRIFT", "severity": "WARNING", "source": "Marketing_Raw", "status": "INVESTIGATING"}
    ]

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "active_pipelines": 142,
        "total_anomalies_24h": 8,
        "unresolved_incidents": 3,
        "avg_mttr_hrs": 4.2
    }

@app.post("/checks/run")
def run_reliability_check(source_id: str):
    logger.info(f"Triggering reliability check for source: {source_id}")
    return {"status": "Analysis Job Enqueued", "job_id": "job_obs_789"}
