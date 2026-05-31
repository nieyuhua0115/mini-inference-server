from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from app.model_runner import IrisModelRunner
from app.request_queue import PredictionQueue


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    model_runner = IrisModelRunner()
    prediction_queue = PredictionQueue(model_runner)
    app.state.prediction_queue = prediction_queue
    await prediction_queue.start()
    try:
        yield
    finally:
        await prediction_queue.stop()


app = FastAPI(lifespan=lifespan)


class PredictRequest(BaseModel):
    features: list[float] = Field(min_length=4, max_length=4)


class PredictResponse(BaseModel):
    class_id: int
    label: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/predict")
async def predict(payload: PredictRequest, request: Request) -> PredictResponse:
    prediction_queue: PredictionQueue = request.app.state.prediction_queue
    prediction = await prediction_queue.predict(payload.features)
    return PredictResponse(class_id=prediction.class_id, label=prediction.label)
