# NikahLens Development Guide

This guide details how to set up, develop, and test NikahLens locally.

## 1. Prerequisites

- **Python**: 3.11+ (Python 3.14 supported)
- **Node.js**: v20+ (v24 supported) & **pnpm**: v9+ (v12 supported)
- **Docker & Docker Compose**: Optional for PostgreSQL (SQLite supported out of the box)

---

## 2. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Default settings use local SQLite (`sqlite:///./nikah_lens.db`). For PostgreSQL:

```bash
# Start PostgreSQL container
docker compose up -d

# Set in .env:
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/nikah_lens
```

---

## 3. Backend Setup & Migrations

Activate the virtual environment:

```bash
source apps/api/.venv/bin/activate
```

Run database migrations:

```bash
alembic -c database/migrations/alembic.ini upgrade head
```

Seed synthetic profiles (35 diverse profiles + default search profiles):

```bash
python database/seed/seed_data.py
```

Run backend server:

```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API docs are available at `http://localhost:8000/docs`.

---

## 4. Frontend Setup

Navigate to `apps/web/`:

```bash
cd apps/web
pnpm install
pnpm dev
```

The web dashboard is available at `http://localhost:3000`.

To create a production build:

```bash
pnpm build
```

---

## 5. Running Tests

Run the complete test suite:

```bash
pytest tests/
```

Tests verify:
- Height, location, age, education, and profession normalizers
- Deen extraction without subjective appraisals
- Deterministic MatchEngine evaluation
- Unknown handling vs disqualification
- Duplicate detection signals and scoring
- Mock adapter profile generation
- REST API integration endpoints
