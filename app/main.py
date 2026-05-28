from fastapi import FastAPI

app = FastAPI(title="Research Aggregator", version="0.1.0")


@app.get("/health")
def health():
    """Liveness check. Confirms the app boots and serves before we add real routes."""
    return {"status": "ok"}