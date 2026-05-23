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
