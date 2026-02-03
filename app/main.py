from fastapi import FastAPI

app = FastAPI(title="Order Processing Service")

@app.get("/health")
async def health_check():
    return {"status": "ok"}