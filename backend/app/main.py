from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router

app = FastAPI(title="BTEC Smart Platform API")

# إعدادات CORS (السماح للواجهة بالاتصال)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*" # للسماح للكل أثناء التطوير
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط الروابط (API Routes)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to BTEC API"}
