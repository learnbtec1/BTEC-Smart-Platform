
# ===================== Paths =====================
$ProjectRoot = "D:\BTEC-backend"
$BackendDir  = Join-Path $ProjectRoot "backend"
$AppDir      = Join-Path $BackendDir "app"
$MainPy      = Join-Path $AppDir "main.py"
$EnvFile     = Join-Path $ProjectRoot ".env"
$VenvPath    = Join-Path $ProjectRoot ".venv"

Write-Host ">> Initializing BTEC Backend at: $ProjectRoot" -ForegroundColor Cyan

# ===================== Folders =====================
if (!(Test-Path $BackendDir)) { New-Item -ItemType Directory -Path $BackendDir | Out-Null }
if (!(Test-Path $AppDir))     { New-Item -ItemType Directory -Path $AppDir     | Out-Null }

# ===================== Package markers =====================
New-Item -ItemType File -Path (Join-Path $BackendDir "__init__.py") -Force | Out-Null
New-Item -ItemType File -Path (Join-Path $AppDir "__init__.py")     -Force | Out-Null

# ===================== .env file =====================
$jwtSecret = [guid]::NewGuid().ToString()
Set-Content -Path $EnvFile -Value @"
ALLOWED_ORIGINS=*
PORT=10000
JWT_SECRET=$jwtSecret
JWT_EXPIRE_MINUTES=60
"@ -Encoding UTF8
Write-Host ">> .env created with fresh JWT secret" -ForegroundColor Green

# ===================== Write main.py (use single-quoted here-string) =====================
$content = @'
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import List, Dict, Any
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import random, uvicorn, os

# Load env
load_dotenv()

APP_TITLE = "BTEC MetaVerse Engine 2500"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "BTEC backend sample: JWT auth, reports, health."

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ===== CORS =====
allow_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
ALLOW_ORIGINS: List[str] = [o.strip() for o in allow_origins_env.split(",")] if allow_origins_env else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== JWT =====
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
security = HTTPBearer()

def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role", "USER")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token subject")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ===== Mock users =====
USERS = {"hamza": "2200", "admin": "admin123"}

# ===== Schemas =====
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    status: str
    user: Dict[str, Any]
    token: str

# ===== Routes =====
@app.get("/", tags=["Root"])
async def root():
    return {"message": "BTEC Backend is Online and Ready", "engine": "FastAPI 0.1xx"}

@app.post("/api/v1/auth/login", tags=["Auth"], response_model=LoginResponse)
async def login_post(body: LoginRequest):
    if body.username in USERS and USERS[body.username] == body.password:
        token = create_access_token({"sub": body.username, "role": "ADMIN"})
        return {"status": "success", "user": {"username": body.username, "role": "ADMIN"}, "token": token}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.get("/api/v1/admin/generate-reports", tags=["Admin"])
async def reports(current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {
        "data": [
            {"id": i, "student": f"BTEC-Student-{i}", "plagiarism": f"{random.randint(1,10)}%"}
            for i in range(1, 11)
        ]
    }

@app.get("/healthz", tags=["Ops"])
async def healthz():
    return {"status": "ok", "service": APP_TITLE, "version": APP_VERSION}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
'@
Set-Content -Path $MainPy -Value $content -Encoding UTF8
Write-Host ">> main.py written successfully" -ForegroundColor Green

# ===================== venv + deps =====================
if (!(Test-Path $VenvPath)) { python -m venv $VenvPath }
& "$VenvPath\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" python-dotenv "python-jose[cryptography]"

# ===================== PYTHONPATH =====================
$env:PYTHONPATH = $BackendDir
Write-Host ">> PYTHONPATH set to: $env:PYTHONPATH" -ForegroundColor Green

# ===================== Firewall (optional) =====================
try {
  if (-not (Get-NetFirewallRule -DisplayName "BTEC Backend 10000" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName "BTEC Backend 10000" -Direction Inbound -Protocol TCP -LocalPort 10000 -Action Allow | Out-Null
    Write-Host ">> Firewall rule created for port 10000" -ForegroundColor Green
  } else {
    Write-Host ">> Firewall rule already exists" -ForegroundColor Yellow
  }
} catch {
  Write-Host ">> Skipping firewall step (insufficient privileges)" -ForegroundColor Yellow
}

# ===================== Run server =====================
Write-Host ">> Starting Uvicorn at http://0.0.0.0:10000 (CTRL+C to stop)" -ForegroundColor Cyan
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 10000 --reload
