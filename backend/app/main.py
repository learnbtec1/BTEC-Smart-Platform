
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/api/v1/auth/login")
def login(payload: LoginRequest):
    # مثال: تحقُّق بسيط
    if payload.username == "hamza" and payload.password == "2200":
        # في مشروعك الحقيقي رجع JWT فعلي
        return {"token": "example-token-123"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/v1/admin/generate-reports")
def generate_reports():
    # مثال استجابة
    return {"reports": ["r1", "r2"], "status": "generated"}

if __name__ == "__main__":
    import uvicorn
    # شغّل Uvicorn من داخل سكريبت، أو استخدم أمر خارجي كما بالأسفل
    uvicorn.run(app, host="0.0.0.0", port=10000)
