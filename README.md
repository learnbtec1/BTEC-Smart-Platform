# 🌐 BTEC Smart Platform  
### **The Future of Vocational Education — 100 Years Ahead**

منصة BTEC Smart Platform ليست مجرد نظام تعليمي…  
إنها **قفزة زمنية** في مستقبل التعليم المهني.  
منصة تتعامل مع البيانات، التقييمات، الذكاء الاصطناعي، والتجربة التعليمية  
كما لو أنها بُنيت في عام 2125 ثم أُعيدت إلى عصرنا.

---

# ✨ Vision  
# 🎯 Mission  
- الذكاء الاصطناعي  
- التقييم الذكي  
- النزاهة الأكاديمية  
- تجربة تعلم سلسة  
- بنية تقنية قابلة للتوسع لعقود قادمة  
---

# 🧬 Core Philosophy  
- **Integrity First** — النزاهة الأكاديمية ليست ميزة، بل أساس.  
---

# 🏗️ System Architecture (2125‑Ready)
---  
  
## Developer automation (اختصار مهام التطوير)  
  
- Bootstrap backend environment (Unix):  
  
```bash  
./scripts/bootstrap.sh  
```  
  
- Bootstrap backend environment (Windows PowerShell):  
  
```powershell  
.\scripts\bootstrap.ps1  
```  
  
- Common handy targets via `Makefile` (root):  
  
```bash  
make setup        # create venv and install deps  
make docker-up    # docker compose up --build  
make backend-run  # run backend with uvicorn  
make backend-test # run backend tests  
```  
  
CI: A GitHub Actions workflow runs backend tests on push/PR: `.github/workflows/backend-ci.yml`.  
  
```

                 ┌──────────────────────────────┐
                 │     Flutter Mobile App        │
                 │  (Students • Teachers • Admin)│
                 └───────────────┬──────────────┘
                                 │
                 ┌───────────────▼──────────────┐
                 │        React Web Portal        │
                 │   (Dashboard • Analytics)      │
                 └───────────────┬──────────────┘
                                 │  HTTPS
                                 ▼
                 ┌────────────────────────────────┐
                 │        FastAPI Backend          │
                 │  Auth • AI • Assessments • DB   │
                 └───────────────┬────────────────┘
                                 │ SQLAlchemy
                                 ▼
                 ┌────────────────────────────────┐
                 │     PostgreSQL (Render Cloud)   │
                 └────────────────────────────────┘

---

# 🧩 Features  
### 🔐 Authentication  
- تسجيل دخول  
- تسجيل مستخدم  
- JWT Tokens  
- Password hashing  

### 🧠 AI‑Powered Modules (Coming Soon)  
- Plagiarism Detection  
- Smart Assessment Engine  
- Audio‑to‑Text Evaluation  
- Learning Analytics  

### 📊 Data Integrity  
- PostgreSQL  
- Alembic migrations  
- Structured schemas  

### 🚀 DevOps  
- GitHub Actions  
- Lint + Test + Deploy  
- render.yaml جاهز للإنتاج  

---

# 📁 Project Structure

وهو الملف الذي يظهر تلقائيًا في الصفحة الرئيسية للمستودع.

---

# 🎉 جاهز الآن  
إذا تريد:

- نسخة إنجليزية  
- نسخة مختصرة  
- نسخة موجهة للمستثمرين  
- نسخة موجهة للطلاب والمعلمين  
- أو إضافة شعار ASCII للمنصة  

فقط اطلب، وأنا أجهّزها لك فورًا.

---

## Generating migrations (local workflow)

A helper PowerShell script is provided to autogenerate Alembic migrations from anywhere inside the repo:

- Script: `backend/scripts/gen_migration.ps1`

Quick steps (PowerShell):

```powershell
# from repo root or backend folder
& .\backend\scripts\gen_migration.ps1

# or provide a DB URL (Postgres example)
& .\backend\scripts\gen_migration.ps1 -DatabaseUrl 'postgresql://user:pass@localhost:5432/dbname'
```

What the script does:
- Detects and uses the `backend` folder (safe path detection).
- Activates `backend/.venv` if present.
- Sets `DATABASE_URL` (uses a local SQLite file by default if none provided).
- Runs `alembic revision --autogenerate -m "add assessments"` and prints the generated file path.

After generation:
1. Review the file created under `backend/app/alembic/versions/`.
2. Apply it with:

```powershell
cd backend
python -m alembic -c alembic.ini upgrade head
```

Notes:
- Inspect the migration before applying — autogenerate can miss manual adjustments (FK `ondelete`, indexes, extensions).
- The code change replacing `.dict()` with `.model_dump()` was applied to `backend/app/services/assessments.py` to avoid SQLModel deprecation warnings.


