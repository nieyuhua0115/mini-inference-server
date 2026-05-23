# AGENTS.md

## Project

This is Mini Inference Server, a production-style AI inference infrastructure side project.

The goal is to build a model serving system with:
- REST inference API
- ModelRunner abstraction
- request queueing
- dynamic batching
- observability
- benchmarking
- Docker
- Kubernetes
- multi-model routing
- vLLM integration

## Engineering Principles

- Keep diffs small and reviewable.
- One task should produce one focused diff.
- Prefer simple, explicit code over clever abstractions.
- Separate API layer, model runtime, batching, metrics, benchmark, and deployment.
- Do not introduce unnecessary dependencies.
- Every behavior should have tests.
- Preserve existing behavior unless the task explicitly changes it.
- Do not build features that are out of scope for the current task.

## Stack

- Python
- FastAPI
- pytest
- uv
- Docker later
- Prometheus later
- Kubernetes later

## Commands

Install dependencies:

uv sync

Run tests:

uv run pytest

Run server:

uv run uvicorn app.main:app --reload

## Diff Rules

Before finishing any task:

1. Run tests.
2. Show changed files.
3. Summarize design decisions.
4. Mention assumptions.
5. Mention skipped tests or known limitations.

## Current Roadmap

1. Project skeleton
2. Health and readiness endpoints
3. Predict endpoint with dummy model
4. ModelRunner abstraction
5. Request queue
6. Dynamic batching
7. Prometheus metrics
8. Benchmark scripts
9. Docker
10. Kubernetes
11. Multi-model routing
12. vLLM integration
