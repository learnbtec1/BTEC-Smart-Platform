<#
build_complete_fixed.ps1
Safer, ASCII-only PowerShell script to prepare and build the project locally.

What it does:
- Creates a backup of docker-compose.yml (if exists).
- Writes a corrected docker-compose.yml for local development.
- Adds frontend helper files if missing:
  - frontend/src/components/Onboarding.tsx
  - frontend/src/lib/api.ts
  - frontend/src/components/ChatWidget.tsx
- Adds backend helper files if missing:
  - backend/scripts/create_superuser.py
  - backend/app/api/chat.py
- Ensures backend/Dockerfile has WORKDIR /app and COPY . /app (minimal safe modification).
- Optionally creates a local git commit (if you confirm).
- Attempts to run docker compose up -d --build and run alembic upgrade head inside backend container.
- Prompts for creating superuser interactively inside the backend container.

Notes / Safety:
- This script uses only ASCII messages to avoid encoding issues.
- It writes files using UTF8 encoding.
- Review generated files before pushing to remote.
- Run from repository root (where docker-compose.yml is located).

Run:
Set-Location 'D:\BTEC-backend'
PowerShell -NoProfile -ExecutionPolicy Bypass -File .\build_complete_fixed.ps1
#>

function WriteStep($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }

# ensure running in repository root
$root = Get-Location
WriteStep "Repository root: $root"

# check prerequisites
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git not found in PATH. Please install Git and retry." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "docker not found in PATH. Please install Docker Desktop and ensure it's running." -ForegroundColor Yellow
    # continue: user may only want file generation
}

# 1) Backup docker-compose.yml
$composePath = Join-Path $root 'docker-compose.yml'
if (Test-Path $composePath) {
    $bakPath = Join-Path $root 'docker-compose.yml.bak'
    Copy-Item -Path $composePath -Destination $bakPath -Force
    WriteStep "Backed up docker-compose.yml -> docker-compose.yml.bak"
} else {
    WriteStep "No docker-compose.yml found; one will be created."
}

# 2) Write a corrected docker-compose.yml
$composeContent = @'
version: "3.9"
services:
  db:
    image: postgres:17-alpine
    container_name: btec-db-v2
    env_file: .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: btec-backend-v2
    env_file: .env
    environment:
      DATABASE_URL: ${DATABASE_URL_INTERNAL}
      PROJECT_NAME: BTEC
      FIRST_SUPERUSER: ${FIRST_SUPERUSER}
      FIRST_SUPERUSER_PASSWORD: ${FIRST_SUPERUSER_PASSWORD}
      PYTHONPATH: /app
    ports:
      - "10000:10000"
    depends_on:
      db:
        condition: service_healthy
    restart: always
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
    volumes:
      - ./backend:/app:delegated

  frontend:
    build: ./frontend
    container_name: btec-frontend-v2
    ports:
      - "3001:3000"
    environment:
      NEXT_PUBLIC_API_URL: "http://localhost:10000"
    depends_on:
      - backend
    restart: always
    volumes:
      - ./frontend:/app:delegated

volumes:
  postgres_data:
'@

Set-Content -Path $composePath -Value $composeContent -Encoding UTF8
WriteStep "Wrote corrected docker-compose.yml (review docker-compose.yml.bak if needed)."

# Helper to write file only if missing
function EnsureFile($path, $content) {
    if (-not (Test-Path $path)) {
        $dir = Split-Path $path
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        Set-Content -Path $path -Value $content -Encoding UTF8
        WriteStep "Added: $path"
    } else {
        WriteStep "Exists: $path (skipped)"
    }
}

# 3) Frontend files
$onboardingPath = Join-Path $root 'frontend\src\components\Onboarding.tsx'
$onboardingContent = @'
import React, { useState, useEffect } from "react";

export default function Onboarding() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const seen = typeof window !== "undefined" && localStorage.getItem("btec_onboard_seen");
    if (!seen) setShow(true);
  }, []);
  if (!show) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-2xl p-6 bg-white dark:bg-neutral-900 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-3">Welcome to the platform</h2>
        <p className="mb-4">Quick tour: search, chat with the helper, and upload files easily.</p>
        <div className="flex justify-end">
          <button className="px-4 py-2 rounded bg-primary text-white" onClick={() => { localStorage.setItem("btec_onboard_seen","1"); window.location.reload(); }}>
            Get started
          </button>
        </div>
      </div>
    </div>
  );
}
'@
EnsureFile $onboardingPath $onboardingContent

$apiPath = Join-Path $root 'frontend\src\lib\api.ts'
$apiContent = @'
const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";

async function request(path: string, opts: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: any = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${BASE}${path}`, { ...opts, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json().catch(() => null);
}

export const api = {
  get: (p: string) => request(p, { method: "GET" }),
  post: (p: string, body?: any) => request(p, { method: "POST", body: JSON.stringify(body) }),
  put: (p: string, body?: any) => request(p, { method: "PUT", body: JSON.stringify(body) }),
  del: (p: string) => request(p, { method: "DELETE" }),
};
'@
EnsureFile $apiPath $apiContent

$chatPath = Join-Path $root 'frontend\src\components\ChatWidget.tsx'
$chatContent = @'
import React, { useState } from "react";
import { api } from "../lib/api";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<{role:string,text:string}[]>([]);
  const [input, setInput] = useState("");

  async function send() {
    if (!input) return;
    const userMsg = { role: "user", text: input };
    setMessages(m => [...m, userMsg]);
    setInput("");
    try {
      const resp = await api.post("/chat", { q: input });
      setMessages(m => [...m, { role: "assistant", text: resp.answer || "Sorry, no answer." }]);
    } catch (e) {
      setMessages(m => [...m, { role: "assistant", text: "Error occurred, try again later." }]);
    }
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open ? (
        <div className="w-80 bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-3">
          <div className="h-48 overflow-auto mb-2">
            {messages.map((m,i) => <div key={i} className={m.role==="user"?"text-right":"text-left"}>{m.text}</div>)}
          </div>
          <div className="flex gap-2">
            <input value={input} onChange={e=>setInput(e.target.value)} className="flex-1 p-2 rounded border" />
            <button onClick={send} className="px-3 py-1 bg-primary text-white rounded">Send</button>
          </div>
        </div>
      ) : null}
      <button onClick={()=>setOpen(s=>!s)} className="w-12 h-12 rounded-full bg-primary text-white shadow-lg">💬</button>
    </div>
  );
}
'@
EnsureFile $chatPath $chatContent

# 4) Backend helper files
$createSuperPath = Join-Path $root 'backend\scripts\create_superuser.py'
$createSuperContent = @'
#!/usr/bin/env python3
"""
Example create_superuser helper.
Run inside backend container:
docker compose exec backend python scripts/create_superuser.py
Adjust imports according to your project structure.
"""
import getpass
try:
    from app import crud, database, schemas
    db = database.SessionLocal()
except Exception:
    print("Warning: could not import project modules directly. Run inside backend container.")
    raise

def main():
    email = input("Email for admin: ").strip()
    pwd = getpass.getpass("Password: ")
    user = crud.get_user_by_email(db, email=email)
    if user:
        print("User exists, updating to superuser...")
        try:
            crud.update_user_to_superuser(db, user)
            print("Updated.")
        except Exception as ex:
            print("Update failed:", ex)
    else:
        try:
            crud.create_user(db, schemas.UserCreate(email=email, password=pwd, is_superuser=True))
            print("Created superuser.")
        except Exception as ex:
            print("Create failed:", ex)

if __name__ == "__main__":
    main()
'@
EnsureFile $createSuperPath $createSuperContent

$chatPyPath = Join-Path $root 'backend\app\api\chat.py'
$chatPyContent = @'
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatIn(BaseModel):
    q: str

@router.post("/")
async def chat_endpoint(payload: ChatIn):
    q = payload.q
    answer = f"Received: {q}. This is a placeholder response."
    return {"answer": answer}
'@
EnsureFile $chatPyPath $chatPyContent

# 5) Ensure backend Dockerfile has WORKDIR and COPY (minimal safe check)
$backendDocker = Join-Path $root 'backend\Dockerfile'
if (Test-Path $backendDocker) {
    $dockerText = Get-Content $backendDocker -Raw
    $modified = $false
    if ($dockerText -notmatch "WORKDIR\s+/app") {
        $dockerText = "WORKDIR /app`n" + $dockerText
        $modified = $true
    }
    if ($dockerText -notmatch "COPY\s+\.\s+/app") {
        $dockerText = $dockerText + "`nCOPY . /app`n"
        $modified = $true
    }
    if ($modified) {
        Set-Content -Path $backendDocker -Value $dockerText -Encoding UTF8
        WriteStep "Patched backend/Dockerfile (added WORKDIR /app and COPY . /app if missing)."
    } else {
        WriteStep "backend/Dockerfile looks fine (no changes)."
    }
} else {
    WriteStep "No backend/Dockerfile found at backend/Dockerfile (skipped patch)."
}

# 6) Offer to create a local git commit
$commitAnswer = Read-Host "Create a local git commit with these changes? (y/n)"
if ($commitAnswer -match '^[Yy]') {
    git add .
    git commit -m "chore: prepare onboarding, chat endpoint, api client and corrected compose" -q
    WriteStep "Local commit created."
} else {
    WriteStep "Skipping local commit."
}

# 7) Try to build and run with docker compose (if docker available)
if (Get-Command docker -ErrorAction SilentlyContinue) {
    WriteStep "Running: docker compose down --remove-orphans"
    docker compose down --remove-orphans
    WriteStep "Running: docker compose up -d --build"
    docker compose up -d --build
    WriteStep "Docker compose started (check containers with 'docker compose ps')."
} else {
    WriteStep "Docker not available; skipped compose up. You can run 'docker compose up -d --build' manually."
}

# 8) Try alembic upgrade head inside backend container (best-effort)
try {
    WriteStep "Attempting alembic upgrade head inside backend container (best-effort)."
    docker compose exec backend sh -c "if command -v alembic >/dev/null 2>&1; then alembic upgrade head || true; else echo 'alembic not found inside container'; fi"
} catch {
    WriteStep "Alembic step skipped or failed (check container manually)."
}

# 9) Offer to run create_superuser inside container
$adminAnswer = Read-Host "Create superuser now inside backend container (interactive)? (y/n)"
if ($adminAnswer -match '^[Yy]') {
    WriteStep "Running create_superuser inside backend container..."
    docker compose exec -it backend python scripts/create_superuser.py
} else {
    WriteStep "Skipping interactive superuser creation. You can run: docker compose exec backend python scripts/create_superuser.py"
}

WriteStep "Script finished. Inspect created files and logs. Review before pushing to remote."