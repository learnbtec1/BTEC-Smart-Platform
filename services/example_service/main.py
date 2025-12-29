from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"service": "example_service", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
