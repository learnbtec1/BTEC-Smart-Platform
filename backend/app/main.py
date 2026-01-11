from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router

app = FastAPI(title="BTEC Smart Platform")

# السماح للجميع (حل جذري لمشكلة الاتصال)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح لأي مصدر
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Server is running on 127.0.0.1"}
