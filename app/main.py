from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.model_runner import DummyModelRunner
from app.request_queue import PredictionQueue

model_runner = DummyModelRunner()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    prediction_queue = PredictionQueue(model_runner)
    app.state.prediction_queue = prediction_queue
    await prediction_queue.start()
    try:
        yield
    finally:
        await prediction_queue.stop()


app = FastAPI(lifespan=lifespan)


class PredictRequest(BaseModel):
    input: str


class PredictResponse(BaseModel):
    output: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/predict")
async def predict(payload: PredictRequest, request: Request) -> PredictResponse:
    prediction_queue: PredictionQueue = request.app.state.prediction_queue
    output = await prediction_queue.predict(payload.input)
    return PredictResponse(output=output)
