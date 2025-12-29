from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Microservices API Gateway", version="1.0.0")

# Load service configurations
SERVICES = json.loads(os.getenv('SERVICES', '{}'))
logger.info(f"Loaded services: {SERVICES}")

# Fallback for local development
if not SERVICES:
    SERVICES = {
        "example_service": "http://localhost:8000",
    }

@app.get("/")
async def root():
    return {
        "gateway": "Microservices API Gateway",
        "services": list(SERVICES.keys()),
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "services": len(SERVICES)}

@app.get("/services")
async def list_services():
    """List all available services"""
    return {"services": SERVICES}

@app.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_proxy(service_name: str, path: str, request: Request):
    """Proxy requests to microservices"""
    
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    service_url = SERVICES[service_name]
    target_url = f"{service_url}/{path}"
    
    # Forward request
    async with httpx.AsyncClient() as client:
        try:
            # Get request body if present
            body = None
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
            
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers.items() 
                        if k.lower() not in ['host', 'connection']},
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            
            return JSONResponse(
                content=response.json() if response.headers.get('content-type', '').startswith('application/json') 
                       else {"response": response.text},
                status_code=response.status_code
            )
            
        except httpx.RequestError as e:
            logger.error(f"Error proxying to {service_name}: {e}")
            raise HTTPException(status_code=503, detail=f"Service '{service_name}' unavailable")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal gateway error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
