# 🧠 Copilot Instructions — BTEC Smart Platform & Backend
These instructions help AI coding agents become productive immediately in this codebase.  
Focus on respecting existing architecture, workflows, and conventions.

---

## 🔷 1. Big Picture Architecture

This project consists of **three coordinated components**:

### **1) Flutter Frontend — `/Flutter`**
- Mobile + Web client for the BTEC Smart Platform.
- Uses:
  - `google_fonts`, `iconsax`, `lottie`, `shimmer`, `fl_chart`
  - Custom assets under `assets/{images,icons,animations,fonts}`
- UI follows a **Cairo font**, clean card-based layout, and modular widgets.
- State management is currently lightweight; avoid introducing new patterns unless requested.

### **2) FastAPI Backend — `/BTEC-backend`**
- Provides AI-powered assessment APIs.
- Organized into:
  - `/routes` → endpoint definitions  
  - `/services` → business logic  
  - `/models` → Pydantic schemas  
  - `/utils` → helpers (validation, scoring, file ops)
- Uses microservice-friendly structure; keep modules isolated.

### **3) Virtual World Submodule — `/BTEC-Virtual-World`**
- Git submodule providing shared assets and simulation templates.
- Always update using:
git submodule update --init --recursive

---

## 🔷 2. Developer Workflows

### **Flutter**
- Install dependencies:





---

## 🔷 3. Project Conventions

### **Flutter**
- Use `Cairo` as the primary font.
- All UI components live under `lib/widgets` or `lib/features/...`.
- Avoid business logic inside widgets; place logic in `services` or `controllers`.

### **Backend**
- Every endpoint must have:
- A Pydantic request model
- A Pydantic response model
- A service function
- Keep routes thin; logic belongs in `/services`.

### **Virtual World**
- Treat as read-only unless explicitly modifying simulation templates.

---

## 🔷 4. Integration Patterns

### **Frontend → Backend**
- All API calls use the `http` package.
- Base URL is configured in `lib/config/api.dart`.
- Responses must be parsed into typed Dart models.

### **Backend → AI Services**
- AI scoring modules live under `/services/ai`.
- Avoid mixing AI logic with routing.

### **Backend → Virtual World**
- Access shared assets via relative imports from the submodule path.

---

## 🔷 5. Important Files & Directories

| Path | Purpose |
|------|---------|
| `/Flutter/pubspec.yaml` | Dependencies, assets, fonts |
| `/Flutter/lib/` | Main application code |
| `/BTEC-backend/routes/` | API endpoints |
| `/BTEC-backend/services/` | Business logic |
| `/BTEC-backend/models/` | Pydantic schemas |
| `/BTEC-Virtual-World/` | Submodule assets |

---

## 🔷 6. Patterns AI Agents Should Follow

- Prefer **small, composable functions** over large monolithic ones.
- Maintain **strict separation** between UI, logic, and data models.
- When adding new endpoints:
- Create a model → service → route (in that order).
- When adding new Flutter screens:
- Create a folder under `lib/features/<feature_name>/`
- Include: `view.dart`, `controller.dart`, `widgets/`

---

## 🔷 7. What NOT to Do

- Do not introduce new state management libraries unless requested.
- Do not modify submodule structure.
- Do not mix backend business logic inside route files.
- Do not place assets outside the defined folders.

---

## 🔷 8. Quick Start for AI Agents

If generating code:

- For Flutter UI → follow existing widget patterns in `lib/widgets`.
- For backend endpoints → mirror structure in `routes/health.py` or similar.
- For models → follow Pydantic style in `models/`.

---

If any section is unclear, request clarification and iterate.