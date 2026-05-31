from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from app.model_runner import IrisModelRunner, ModelRunner
from app.request_queue import PredictionQueue


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    model_runner = IrisModelRunner()
    prediction_queue = PredictionQueue(model_runner)
    app.state.model_runner = model_runner
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


class ModelMetadataResponse(BaseModel):
    name: str
    version: str
    task: str
    input_schema: dict[str, str]
    output_schema: dict[str, str]


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/models/current")
def current_model(request: Request) -> ModelMetadataResponse:
    model_runner: ModelRunner = request.app.state.model_runner
    metadata = model_runner.metadata()
    return ModelMetadataResponse(
        name=metadata.name,
        version=metadata.version,
        task=metadata.task,
        input_schema=metadata.input_schema,
        output_schema=metadata.output_schema,
    )


@app.post("/predict")
async def predict(payload: PredictRequest, request: Request) -> PredictResponse:
    prediction_queue: PredictionQueue = request.app.state.prediction_queue
    prediction = await prediction_queue.predict(payload.features)
    return PredictResponse(class_id=prediction.class_id, label=prediction.label)
