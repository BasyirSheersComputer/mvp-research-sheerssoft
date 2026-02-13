# SheersSoft AI Inquiry Capture & Conversion Engine

An AI-powered hotel inquiry capture system that recovers revenue lost after hours.

## Architecture

- **Backend:** Python 3.12 + FastAPI (single container)
- **Database:** PostgreSQL 16 + pgvector (semantic search)
- **LLM:** OpenAI GPT-4o-mini
- **Channels:** WhatsApp (Meta Cloud API), Web Chat Widget, Email (SendGrid)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API key

### 1. Clone and configure
```bash
cd backend
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Start services
```bash
docker compose up -d
```

This starts:
- PostgreSQL 16 with pgvector extension (port 5432)
- FastAPI backend with hot-reload (port 8000)

### 3. Seed the pilot property (Vivatel KL)
```bash
docker compose exec backend python -m scripts.seed_vivatel
```

### 4. Test the AI
```bash
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "<property-id-from-seed>",
    "message": "Hi, do you have rooms available this weekend?"
  }'
```

### API Documentation
Once running, visit: http://localhost:8000/docs

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Environment configuration
│   │   ├── database.py          # Async SQLAlchemy engine
│   │   ├── models.py            # Database models (6 entities)
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── routes.py            # All API endpoints
│   │   └── services/
│   │       ├── __init__.py      # KB ingestion + RAG search
│   │       ├── conversation.py  # AI conversation engine
│   │       └── analytics.py     # Daily analytics aggregation
│   ├── scripts/
│   │   └── seed_vivatel.py      # Pilot property seed data
│   ├── alembic/                 # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── docs/                        # Research & playbooks
├── docker-compose.yml
└── .gitignore
```

## Sprint Status

- [x] **Sprint 1:** AI Conversation Core (The Brain Works)
- [x] **Sprint 2:** WhatsApp + Web Widget + Email (Guests Can Reach Us)
- [x] **Sprint 3:** Dashboard + Analytics + Reports (The GM Sees the Money)
- [/] **Sprint 4:** Polish + Deploy + Pilot (Go Live at Vivatel)



