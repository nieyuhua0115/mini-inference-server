from fastapi import FastAPI
from pydantic import BaseModel

from app.model_runner import DummyModelRunner

app = FastAPI()
model_runner = DummyModelRunner()


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
def predict(request: PredictRequest) -> PredictResponse:
    output = model_runner.predict(request.input)
    return PredictResponse(output=output)
