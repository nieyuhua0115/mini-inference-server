# Mini Inference Server

A production-style AI inference infrastructure side project.

The long-term goal is to build a model serving system with:

- REST inference API
- ModelRunner abstraction
- request queueing
- dynamic batching
- Prometheus metrics
- benchmarking
- Docker deployment
- Kubernetes deployment
- multi-model routing
- vLLM-backed LLM serving

This repository is also built with an AI-native engineering workflow:

Task spec → isolated branch/worktree → AI implementation → diff review → tests → PR → merge.

## Local setup

Install dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Run the development server:

```bash
uv run uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/healthz
```

Readiness check:

```bash
curl http://127.0.0.1:8000/readyz
```

Dummy prediction:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"input": "hello"}'
```
